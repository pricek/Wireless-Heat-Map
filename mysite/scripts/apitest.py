import requests
import os.path as path
import time
import data.strings as creds

def createKey():
    keyAge = path.getmtime('api_access.txt') if path.exists('api_access.txt') else 0
    now = time.time()
    if now - keyAge > 86399:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        }

        data = {
        'grant_type': 'client_credentials',
        'client_id': creds.GetLocationsClientID,
        'client_secret': creds.GetLocationsClientSecret
        }

        response = requests.post('https://api.oregonstate.edu/oauth2/token', headers=headers, data=data)
        key = response.json()
        f=open("api_access.txt", "w+")
        f.write("%s" % key['access_token'])
        f.close()
