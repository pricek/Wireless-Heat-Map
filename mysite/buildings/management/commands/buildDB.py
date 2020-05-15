from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from buildings.models import Building, Floor, Room
from scripts.helpers import Building_Helper
from scripts import pull_airwave
import logging
import os
import json
    
BASE_DIR = settings.BASE_DIR
LOCAL_DIR = os.path.dirname(__file__)

class Command(BaseCommand):
    help = 'Builds the database from a data dump'
    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear the database instead of building it')
        parser.add_argument('--render', action='store_true', help='Populates render information for the database instead of building it')
        parser.add_argument('--derender', action='store_true', help='Removes render information for the database instead of building it')
        parser.add_argument('--baseline', action='store_true', help='Sets baseline values in the database')
        parser.add_argument('--floor', action='store_true', help='Works on floors instead of Buildings')
        parser.add_argument('--room', action='store_true', help='Works on rooms instead of Buildings')

    def handle(self, *args, **options):
        if options['room']:
            objs = Room.objects
        elif options['floor']:
            objs = Floor.objects
        else:
            objs = Building.objects
        BH = Building_Helper()
        if options['clear']:
            objs.all().delete()
        elif options['derender']:
            hasri = objs.filter(has_render=True)
            for loc in hasri:
                loc.has_render = False
                loc.save()
        elif options['render']:
            ri = BH.get_render_info()
            nori = Building.objects.filter(has_render=False)
            path = os.path.join(BASE_DIR, "logs/render.log") 
            f=open(path, "w")
            for loc in nori:
                BH.load_build_render(ri, loc)
                loc.save()
            f.close()
        elif options['baseline']:
            for loc in Building.objects.all():
                for f in loc.floor_set.all():
                    loc.baseline_clients += f.baseline_clients
                for r in loc.room_set.all():
                    loc.baseline_clients += r.baseline_clients
                loc.save()
                #print("placeholder")
        else:
            builds = pull_airwave.pull_data()
            BH.reset_baseline_clients()
            for bs in builds:
                b = builds[bs]
                BH.add_location(b, builds)
            print(BH.count)



