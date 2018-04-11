import requests
import json
import time
import shutil
import os
import re

API_KEY =  'KEY'
PARMS = {'key': API_KEY, 'animal': 'dog', 'output':'full', 'format':'json', 'location':'22901', 'count':150}

while 1:
    shutil.rmtree('./pf-img/',ignore_errors=True)
    os.mkdir('./pf-img')
    r = requests.get('http://api.petfinder.com/pet.find',params=PARMS)
    if r.status_code != 200:
        continue
    for pet in json.loads(r.text)['petfinder']['pets']['pet']:
        pet_name = re.sub(r'[^a-zA-Z0-9 ]', '', pet['name']['$t'])
        pet_id = pet['id']['$t']
        if pet['status']['$t'] != "A":
            print("Not available! "+pet_id)
        with open("pf-img/"+pet_id+"-"+pet_name+".txt", 'w') as f:
            f.write(json.dumps(pet))
        try:
            n=0
            for photo in pet['media']['photos']['photo']:
                if photo['@size'] == 'x':
                    img_url = photo['$t']
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        with open("pf-img/"+pet_id+"-"+pet_name+"-"+str(n)+".jpg", 'wb') as f:
                            for chunk in img_response:
                                f.write(chunk)
                    n+=1
        except KeyError:
            # No photo for doggo :(
            continue

    time.sleep(86400)
