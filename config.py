filePaths = dict(
    cities='./cache/cities.json',
    articlesPerCity='./cache/articles-per-city.json',
    articles='./cache/cities/',
    mapIds='./data/names-and-ids.json',
    mapJs='./cache/color-map.js'
)

#These cities have merged and are displayed as one administrative regionn on the map
replaceCityNames = {
    'Aarau Rohr': 'Aarau',
    'Attelwil': 'Reitnau',
    'Kleindottingen': 'Bottstein',
    'Hottwil': 'Mettauertal',
    'Scherz': 'Lupfig',
    'Schinznach-Bad': 'Brugg',
    'Bozberg (Unter-/Oberbozberg, Linn, Gallenkirch)': 'Bozberg',
    'Obersiggenthal (Nussbaumen)': 'Obersiggenthal',
}

#These cities are in solothurn, yet appear in aargauerzeitung's city list
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
]

maxArticlesPerCity = 250

def get_cache_path(cityData):
    return filePaths['articles'] + str(cityData['id']) + '-' + cityData['urlpart'] + '.json'
