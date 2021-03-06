import requests
import json
from config import filePaths

filePath = filePaths['cities']

URL = 'https://www.aargauerzeitung.ch/__node__/__api__/cities'
PARAMS = {'limit': 1000}
r = requests.get(url = URL, params = PARAMS)
# var dict data
data: dict = r.json()

with open(filePath, 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)

print(str(len(data['data'])) + ' Cities')
