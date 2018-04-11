import requests
import json
from io import BytesIO
import time

PARMS = {'key': 'API_KEY', 'animal': 'dog', 'output':'full', 'format':'json'}

while 1:
    for n in range(500):
        r = requests.get('http://api.petfinder.com/pet.getRandom',params=params)
        try:
            #id = json.loads(r.text)['petfinder']['pet']['id']['$t']
            for p in json.loads(r.text)['petfinder']['pet']['media']['photos']['photo']:
                if p['@size'] == 'x':
                    img_url = p['$t']
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        with open("pf-img/"+str(n)+".jpg", 'wb') as f:
                            for chunk in img_response:
                                f.write(chunk)
                    break
        except KeyError:
            # No photo for doggo :(
            continue
        time.sleep(1)
    time.sleep(86400)
