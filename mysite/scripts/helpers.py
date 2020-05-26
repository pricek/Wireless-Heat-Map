from buildings.models import Building, Floor, Room
from influxdb import InfluxDBClient
from .external import Regex_Helper
from scripts import getLocations
import re
import os
import xmltodict
import json
import colorsys
import datetime

#Helper object used to work with building information
class Building_Helper:
    RH = Regex_Helper()
    abbrRE = RH.abbrRE
    buildRE = RH.buildRE
    floorRE = RH.floorRE
    roomRE  = RH.roomRE
    count = 0

    #Sets the baseline client value for all locations
    def reset_baseline_clients(self):
        buildings = Building.objects.all()
        floors = Floor.objects.all()
        rooms = Room.objects.all()
        for temp in [buildings,floors,rooms]:
            for obj in temp:
                obj.baseline_clients = 0
                obj.save()
    
    #Reads data from a data dump from Airwave
    def read_data(self, data_path):
        f = open(data_path, "r")
        myxml = f.read()
        f.close

        temp = xmltodict.parse(myxml)
        temp_locs = temp['amp:amp_folder_list']['folder']
        locs = {l['@id'] : l for l in temp_locs}
        return locs

    #Adds a building to the database with a given building number, name, and baseline clients
    #Updates the name of a building if a building with the given number exists
    def add_building(self, number, name="", bc=0):
        try:
            newBuilding = Building.objects.get(number=number)
            newBuilding.baseline_clients += bc
            if name != "" and newBuilding.name == "":
                newBuilding.name = name
        except Building.DoesNotExist:
            newBuilding = Building(name=name, number=number, baseline_clients=bc)
        newBuilding.save()
        return newBuilding

    #Adds a floor to the database with a given floor number, building, and baseline clients
    def add_floor(self, number, bn, bc=0):
        building = self.add_building(bn)
        try:
            newFloor = Floor.objects.get(building=building, number=number)
            newFloor.baseline_clients += bc
        except Floor.DoesNotExist:
            newFloor = Floor(number=number, building=building, baseline_clients=bc)
        newFloor.save()
        return newFloor, building

    #Adds a room to the database with a given room number, floor, building, and baseline clients
    def add_room(self, number, fn, bn, bc=0):
        if fn is not None:
            floor, building= self.add_floor(fn, bn)
        elif bn is not None:
            floor = None
            building = self.add_building(bn)
        try:
            newRoom = Room.objects.get(building=building, floor=floor, number=number)
            newRoom.baseline_clients += bc
        except Room.DoesNotExist:
            newRoom = Room(number=number, building=building, floor=floor, baseline_clients=bc)
        newRoom.save()
        return newRoom, floor, building

    #Gets the parent of the given location from the provided locations
    def get_parent(self, loc, locs):
        if 'parent_id' in loc:
            pLoc = locs[loc['parent_id']]
        else:
            return None
        
    #Adds a location to the database
    def add_location(self, loc, locs):
        name = loc['name']
        aps = int(loc['up']) + int(loc['down'])
        test = self.abbrRE.search(name)
        if test:
            abbr = test[1]
            temp_building = self.buildRE.search(abbr)
            if temp_building:
                bdict = temp_building.groupdict()
                abbr = bdict['abbr']
                build = bdict['building']
                floor = bdict['floor']
                room = bdict['room']
                if build is None:
                    print(f'Name: {name}')
                    self.count += 1
                    return None
        else:
            self.count += 1
            if aps > 0:
                print("Name: " + loc['name'] + ", APs: " + str(aps))
            return None
        baseline_clients = aps * 15
        if room is not None:
            location = self.add_room(room, floor, build, baseline_clients)
        elif floor is not None:
            location = self.add_floor(floor, build, baseline_clients)
        else:
            location = self.add_building(build, name, baseline_clients)
        return location
    
    #Gets the render information for all OSU locations
    def get_render_info(self):
        def temp_get_abbr(name):
            test = self.abbrRE.search(name)
            abbr = test[1] if test else name
            return abbr
        tempD = json.loads(getLocations.getLocs())
        return tempD
    
    #Gets the render information for the specific location from the provided list of render information
    def load_build_render(self, ri, loc):
        lri = ri.get(loc.number)
        if lri and lri['geometry']['type'] != None:
            loc.render = json.dumps(lri)
            loc.has_render = True

#Objects used to read information from the InfluxDB database
class Database_Reader:
    #Reads the building information from the InfluxDB database
    def read_buildings(self, q_date=datetime.date.today()):
        renders = Building.objects.filter(has_render=True)
        loads = []
        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'airwave_data')
        print(q_date, datetime.date.today())
        #Determines whether request is for current data or archived data.
        if q_date==datetime.date.today().isoformat():
            print("if")
            q_from = 'ap_usage'
            q_where = 'time > now() - 15m'
        else:
            tmp_date = int(datetime.datetime.fromisoformat(q_date).timestamp() * 1000000000)
            print("else", tmp_date)
            q_from = 'one_year.downsampled'
            q_where = 'time >= ' + str(tmp_date) + ' and time < ' + str(tmp_date) + ' + 24h'
        #Queries the InfluxDB database
        print(q_where)
        result = client.query('select sum(clients) as clients, sum(bandwidth_in) as band_in, sum(bandwidth_out) as band_out from ' + q_from + ' where ' + q_where + ' group by building')
        k = [key[1] for key in result.keys()]
        r = [res for res in result.get_points()]
        out = zip(k,r)
        temp = []
        for o in out:
            x = o[0]
            x.update(o[1])
            temp.append(x)
        #Loads the stored render information and maps the data to google maps objects
        for res in temp:
            build = res['building']
            try:
                loc = renders.get(number=build)
            except Building.DoesNotExist:
                continue
            r = json.loads(loc.render)
            try:
                percent_clients = float(res['clients']) / float(loc.baseline_clients)
            except:
                percent_clients = 1
            if percent_clients >= 1: percent_clients=1
            
            # Mapping of the color to a hsl cylinder
            hue = (230-(230 * percent_clients))/ 360
            lightness = 0.5
            saturation = 0.8
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            color = '#%02x%02x%02x' % (round(rgb[0]*255), round(rgb[1]*255), round(rgb[2]*255))

            r['color'] = color
            r['clients'] = res['clients']
            loads.append(r)
        return loads
