import requests
import json
from scripts import apitest

def getLocs():
    apitest.createKey()

    f=open('api_access.txt', 'r')

    key = f.read()
    f.close()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'Bearer '+key,
    }

    params = (
        #('type', 'building'),
        ('page[size]', '10000'),
        #('campus', 'corvallis'),
    )

    response = requests.get('https://api.oregonstate.edu/v1/locations', headers=headers, params=params)
    locations = response.json()

    #This builds a dictionary that can be used to generate a python dictionary that can be used to store in the database
    locs = {x['attributes']['bldgID'] #Sets dictionary keys as building abbreviations
            : 
            {   
                #Place all information that needs to be saved to the databse in this dictionary using the below format
                #'key_name' : value,
                'geometry' : x['attributes']['geometry'],
                'name' : x['attributes']['name'],
                'abbr' : x['attributes']['abbreviation'],
            }      
            for x in locations['data']}
    #f=open('locs.json', 'w')
    out = json.dumps(locs)
    return out
    #f.write(out)
    #f.close()
