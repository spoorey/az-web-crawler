import json
import requests
import datetime
import time
import config
from config import get_cache_path
from config import maxArticlesPerCity
from config import filePaths

def get_first_created(data):
    first = 0
    for entry in data['data']:
        created = entry['dc']['created']
        created = created[:10]
        created = datetime.datetime.strptime(created, '%Y-%m-%d')

        if (first == 0) or (created < first):
            first = created
    return first

def extract_articles(data, minTimestamp, maxAmount, articles):
    for entry in data['data']:
        created = entry['dc']['created'][:10]
        created = datetime.datetime.strptime(created, '%Y-%m-%d')
        if (len(articles) >= maxAmount) or (created < minTimestamp):
            return articles
        articles.append(entry)
    return articles


file = open(filePaths['cities'])
cities = json.load(file)
cities = cities['data']

baseUrl = 'https://www.aargauerzeitung.ch/__node__/__api__/gemeinde/'
threeMonthsAgo = datetime.datetime.today() - datetime.timedelta(3*365/12)
print(threeMonthsAgo)

i = 0
for city in cities:
    i = i+1
    articles = []

    page = 0
    print('('+ str(i) +'/' + str(len(cities)) + ') ' + city['name'])
    while (True and len(articles)<maxArticlesPerCity):
        # load next page
        page += 1
        print('page ' + str(page))
        time.sleep(0.5)
        url = baseUrl + str(city['id']) + '/seite/' + str(page)

        filePath = get_cache_path(city)
        r = requests.get(url, {})
        data: dict = r.json()

        articles = extract_articles(data, threeMonthsAgo, maxArticlesPerCity, articles)
        created = get_first_created(data)
        if (len(articles)>=maxArticlesPerCity) or (created < threeMonthsAgo):
            print('found ' + str(len(articles)) + ' articles since ' + threeMonthsAgo.isoformat())
            break

    with open(filePath, 'w') as outfile:
        json.dump(articles, outfile)
        print('saved to ' + filePath)

