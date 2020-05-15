from .external import Regex_Helper
import airwaveapiclient
from influxdb import InfluxDBClient
import time
import xmltodict
import os
import data.strings as creds

RH = Regex_Helper

#Collects data from airwave API and returns a json object representation of the retrived data
def pull_data():
    data = {}
    print("Start time:" + str(time.time()))
    servers = [
        'https://airwave.nws.oregonstate.edu',
    ]
    for s in servers:
        airwave = airwaveapiclient.AirWaveAPIClient(
                    username=creds.AirwaveUsername,
                    password=creds.AirwavePassword,
                    url=s)
        airwave.login()
        url = airwave.api_path('folder_list.xml')
        result = airwave.session.get(url, verify=False)
        temp_data = result.text
        airwave.logout()
    
        temp = xmltodict.parse(temp_data)
        temp = temp['amp:amp_folder_list']['folder']
        data.update({d['@id'] : d for d in temp})
    return data

#Inserts ap data into the influx db database
def insert_data():
    data = pull_data()
    #in_time = int(time.localtime())

    in_data = []

    for ids,locs in data.items():
        test = RH.abbrRE.search(locs['name'])
        if test:
            abbr = test[1]
            tb = RH.buildRE.search(abbr)
            if tb:
                bdict = tb.groupdict()
                abbr = bdict['abbr']
                build = bdict['building']
                floor = bdict['floor']
                room = bdict['room']
                if build is None:
                    continue
            else:
                continue
        else:
            continue

        point = {
                    "measurement":"ap_usage",
                    "tags": {
                        "uniq":ids,
                        "building":build,
                        "floor":floor,
                        "room":room,
                    },
                    #"time":in_time,
                    "fields": {
                        "clients":int(locs["client_count"]),
                        "bandwidth_in":int(locs["bandwidth_in"]),
                        "bandwidth_out":int(locs["bandwidth_out"]),
                    },
                }
        in_data.append(point)

    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'airwave_data')
    client.write_points(in_data)
    print("success")


