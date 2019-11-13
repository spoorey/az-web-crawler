import requests
import json

filePath = './cache/cities.json'

URL = 'https://www.aargauerzeitung.ch/__node__/__api__/cities'
PARAMS = {'limit': 1000}
r = requests.get(url = URL, params = PARAMS)
# var dict data
data: dict = r.json()

with open(filePath, 'w') as outfile:
    json.dump(data, outfile)

print(len(data['data']))
print('Cities')
