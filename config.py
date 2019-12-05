filePaths = dict(
    cities='./cache/cities.json',
    articles='./cache/cities/'
)

def get_cache_path(cityData):
    return filePaths['articles'] + str(cityData['id']) + '-' + cityData['urlpart'] + '.json'
