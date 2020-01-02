filePaths = dict(
    cities='./cache/cities.json',
    articlesPerCity='./cache/articles-per-city.json',
    articles='./cache/cities/',
    mapIds='./data/names-and-ids.json',
    mapJs='./data/color-map.js'
)

maxArticlesPerCity = 250

def get_cache_path(cityData):
    return filePaths['articles'] + str(cityData['id']) + '-' + cityData['urlpart'] + '.json'
