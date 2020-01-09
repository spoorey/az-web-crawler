import json
import config
from config import get_cache_path
from config import filePaths
import unidecode
import colorcodes
import sys

with open(filePaths['cities'], 'r', encoding='utf8') as file:
    cities = json.load(file)

mapIds = []
with open(filePaths['mapIds'], 'r') as file:
    mapIds = json.load(file)
    for key in mapIds:
        mapIds[key] = unidecode.unidecode(mapIds[key])

# load inhabitant counts
inhabitants = {}
with open(filePaths['inhabitants'], 'r') as file:
    file = json.load(file)
    for key in file:
        cityName = unidecode.unidecode(key)
        cityName = cityName.replace(' (AG)', '')
        inhabitants[cityName] = file[key]

# map console arguments
argv = {}
for value in sys.argv:
    split = value.split('=')
    if (len(split)==2):
        argv[split[0]] = split[1]

perInhabitant = ('mode' in argv) and (argv['mode'] == 'per-inhabitant')

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
        if (not perInhabitant and cityName in config.ignoreCities):
            continue

        key = list(mapIds.keys())[list(mapIds.values()).index(cityName)]
        if (key not in articlesPerKey):
            articlesPerKey[key] = []

         # avoid duplicate article counts by checking the article id
        for article in cityData:
            if (article['id'] not in articlesPerKey[key]):
                articlesPerKey[key].append(article['id'])

        cityInhabitants = inhabitants[cityName]
        articlesCount = len(articlesPerKey[key])
        if (perInhabitant):
            articlesCount = articlesCount/cityInhabitants
        if (articlesCount > maxArticlesPerKey):
            maxArticlesPerKey = articlesCount

# sort data by article count
data = sorted(data, key=lambda data: data['articles'],reverse=True)  

# output as json and javascript
with open(filePaths['articlesPerCity'], 'w') as outfile:
    json.dump(data, outfile)

if (perInhabitant):
    perInhabitantText = ' pro Einwohner'
else:
    perInhabitantText = ''

# text titles
js = 'document.getElementById(\'max-articles\').innerHTML=\'' + str(maxArticlesPerKey) + '\';\n'
js += 'document.getElementById(\'title\').textContent += \''+ perInhabitantText + '\';\n'

if ('color' in argv):
    colorArg = argv['color']
else:
    colorArg = ''
maxColor = colorcodes.colorcode_by_argv(colorArg, maxArticlesPerKey, maxArticlesPerKey)
minColor = colorcodes.colorcode_by_argv(colorArg, 0, maxArticlesPerKey)
midColor =  colorcodes.colorcode_by_argv(colorArg, maxArticlesPerKey/2, maxArticlesPerKey)

# color the gradient on the right
js += 'document.getElementById(\'gradient\').style.backgroundImage = \'linear-gradient(to bottom, #' + maxColor + ', #'+ midColor + ', #' + minColor + ')\';\n'

# color the paths
for key in articlesPerKey:
    cityInhabitants = inhabitants[mapIds[key]]

    articlesCount = len(articlesPerKey[key])
    if (perInhabitant):
        articlesCount = articlesCount/cityInhabitants

    color = colorcodes.colorcode_by_argv(colorArg, articlesCount, maxArticlesPerKey)
    # for each path: name of city, absolute amount of articles (or articles per inhabitant), share of articles (defines color shade)
    js += '//' + mapIds[key] + ': ' + str(articlesCount) + '('+ str(articlesCount/maxArticlesPerKey) + ') articles\n'
    js += 'document.getElementById(\'' + key + '\').style.fill = \'#' + color + '\';\n'
    js +=  'document.getElementById(\'' + key + '\').style.fillOpacity = 1\n'


# add a table with all the data
table = '<table><tr><th>Ort</th><th>Anzahl Artikel'+ perInhabitantText + ' (Maximum: ' + str(config.maxArticlesPerCity) + ')</th>'
for city in data:
    articlesCount = city['articles']
    cityName = city['city'].replace(' (AG)', '')
    if (perInhabitant):
        if (cityName in inhabitants):
            articlesCount = articlesCount/inhabitants[cityName]
            articlesCount = round(articlesCount, 3)
        else:
            articlesCount = 'n/a'

    table += '<tr><td>' + city['city'] + '</td><td>' + str(articlesCount) + '</td>'
table += '</table>'

js += 'document.getElementById(\'article-count\').innerHTML = \'' + table + '\'\n'
with open(filePaths['mapJs'], 'w', encoding='utf8') as outfile:
    outfile.write(js)
print('map ready, open vendor/map.html in your browser')
