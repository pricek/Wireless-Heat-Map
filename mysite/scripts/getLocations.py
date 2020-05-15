import requests
import json
from scripts import apitest

def getLocs():
    apitest.createKey()
    #get most current api key from the api_access.txt file
    f=open('api_access.txt', 'r')
    key = f.read()
    f.close()
    #headers for the request to ensure it is formatted correctly and authorized.
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'Bearer '+key,
    }
    #parameters for the request to the OSU GetLocations API with commented out additional options for filtering
    #based on the site desired for later development
    params = (
        #('type', 'building'),
        ('page[size]', '10000'),
        #('campus', 'corvallis'),
    )
    #request to OSU's GetLocations API that returns a json object with all the locations and their information
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
    out = json.dumps(locs)
    return out
