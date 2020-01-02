import json
import config
from config import get_cache_path
from config import filePaths
import unidecode
import colorcodes
import sys

with open(filePaths['cities'], 'r') as file:
    cities = json.load(file)

mapIds = []
with open(filePaths['mapIds'], 'r') as file:
    mapIds = json.load(file)
    for key in mapIds:
        mapIds[key] = unidecode.unidecode(mapIds[key])
            
data = []
articlesPerKey = {}
maxArticlesPerKey = 0
for city in cities['data']:
    filePath = get_cache_path(city)

    with open(filePath) as cityFile:
        cityData = json.load(cityFile)
        data.append({
            "zip":int(city['zips'][0]),
            "city":city['name'],
            "articles": len(cityData)
        })
        # Avoid problems with umlauts and the (AG)
        cityName = city['name'].replace(' (AG)', '')
        cityName = unidecode.unidecode(cityName)

        # replace or skip cities according to the map (merged cities, cities in solothurn etc.)
        if (cityName in config.replaceCityNames):
            cityName = config.replaceCityNames[cityName]
        if (cityName in config.solothurnCities):
            continue
        if (cityName == 'Aarau'):
            continue

        key = list(mapIds.keys())[list(mapIds.values()).index(cityName)]
        if (key not in articlesPerKey):
            articlesPerKey[key] = []

         # avoid duplicate article counts by checking the article id
        for article in cityData:
            if (article['id'] not in articlesPerKey[key]):
                articlesPerKey[key].append(article['id'])

        if (len(articlesPerKey[key]) > maxArticlesPerKey):
            maxArticlesPerKey = len(articlesPerKey[key])

# sort data by article count
data = sorted(data, key=lambda data: data['articles'],reverse=True)  

# output as json and javascript
with open(filePaths['articlesPerCity'], 'w') as outfile:
    json.dump(data, outfile)

js = ''
for key in articlesPerKey:
    articlesCount = len(articlesPerKey[key])
    color = colorcodes.colorcode_by_argv(sys.argv[1], articlesCount, maxArticlesPerKey)
    js += '//' + mapIds[key] + ': ' + str(articlesCount) + '('+ str(articlesCount/maxArticlesPerKey) + ') articles\n'
    js += 'document.getElementById(\'' + key + '\').style.fill = \'#' + color + '\';\n'
    js +=  'document.getElementById(\'' + key + '\').style.fillOpacity = 1\n'

with open(filePaths['mapJs'], 'w') as outfile:
    outfile.write(js)
print('map ready, open vendor/map.html in your browser')
print('The 10 cities with most articles are:')
i = 0
while (i < 11):
    print(data[i]['city'] + ': ' + str(data[i]['articles']) + ' articles')
    i=i+1