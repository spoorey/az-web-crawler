import json

with open('./cache/cities.json', 'r') as file:
    cities = json.load(file)

data = []
for city in cities['data']:
    print(city['name'])
    filePath = basePath + str(city['id']) + '-' + city['urlpart'] + '.json'
    print(filePath)