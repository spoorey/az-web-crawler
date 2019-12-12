import json
import config
from config import get_cache_path
from config import filePaths

with open(filePaths['cities'], 'r') as file:
    cities = json.load(file)

data = {}
for city in cities['data']:
    filePath = get_cache_path(city)
    with open(filePath) as cityFile:
        cityData = json.load(cityFile)
        print(city['name'] + ' ' + str(len(cityData)))
        data[int(city['zips'][0])] = len(cityData)
