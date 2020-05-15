from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from scripts.helpers import Database_Reader

from .models import Building
from .forms import DateForm, NameForm

import data.strings as creds

import json
import datetime

def index(request):
    DBR = Database_Reader()
    building_values = DBR.read_buildings(request.GET.get('select_date',default=datetime.date.today().isoformat()))
    date_form = DateForm(request.GET)
    if not date_form.is_valid():
        date_form = DateForm()
    form = NameForm()
    template = loader.get_template('buildings/index.html')
    context = {
                'form' : form,
                'date_form' : date_form,
                'location_data' : building_values, 
                'api_key': creds.GoogleMapsAPIKey,}
    return HttpResponse(template.render(context, request))

# Create your views here.
