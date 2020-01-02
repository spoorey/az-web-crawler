import json
import config
from config import get_cache_path
from config import filePaths
import unidecode

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
        cityName = city['name'].replace(' (AG)', '')
        cityName = unidecode.unidecode(cityName)

        #These cities have merged or are displayed as one on the map
        replaceCityNames = {
            'Aarau Rohr': 'Aarau',
            'Attelwil': 'Reitnau',
            'Kleindottingen': 'Bottstein',
            'Hottwil': 'Mettauertal',
            'Scherz': 'Lupfig',
            'Schinznach-Bad': 'Brugg',
            'Bozberg (Unter-/Oberbozberg, Linn, Gallenkirch)': 'Bozberg',
        }
        if (cityName in replaceCityNames):
            cityName = replaceCityNames[cityName]
        
        #These cities are in solothurn
        solothurnCities = [
            'Daniken',
            'Dietikon',
            'Dulliken',
            'Eppenberg-Woschnau',
            'Erlinsbach SO',
            'Gretzenbach',
            'Hagendorf',
            'Kienberg',
            'Lostorf',
            'Niedergosgen',
            'Obergosgen',
            'Nussbaumen',
            'Stusslingen',
            'Schonenwerd',
            'Obersiggenthal (Nussbaumen)',
        ]

        if (cityName in solothurnCities):
            continue
        
        key = list(mapIds.keys())[list(mapIds.values()).index(cityName)]
        if (key not in articlesPerKey):
            articlesPerKey[key] = []

         # avoid duplicate article counts
        for article in cityData:
            if (article['id'] not in articlesPerKey[key]):
                articlesPerKey[key].append(article['id'])
        if (len(articlesPerKey[key]) > maxArticlesPerKey):
            maxArticlesPerKey = maxArticlesPerKey+len(articlesPerKey[key])
with open(filePaths['articlesPerCity'], 'w') as outfile:
    json.dump(data, outfile)

js = ''
for key in articlesPerKey:
    articlesCount = len(articlesPerKey[key])
    color = (articlesCount/maxArticlesPerKey)* int('ffff',16)
    color = format(int(color), 'X')
    color = color.rjust(4, '0')
    js += 'document.getElementById(\'' + key + '\').style.fill = \'#' + color +'FF\';\n'
    js +=  'document.getElementById(\'' + key + '\').style.fillOpacity = 1\n'

with open(filePaths['mapJs'], 'w') as outfile:
    outfile.write(js)