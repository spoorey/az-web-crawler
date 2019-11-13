import json
import requests
import datetime
import time

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
        if (len(articles) > maxAmount) or (created < minTimestamp):
            return articles
        articles.append(entry)
    return articles


file = open('./cache/cities.json')
cities = json.load(file)
cities = cities['data']

basePath = './cache/cities/'
baseUrl = 'https://www.aargauerzeitung.ch/__node__/__api__/gemeinde/'
threeMonthsAgo = datetime.datetime.today() - datetime.timedelta(3*365/12)
print(threeMonthsAgo)


for city in cities:
    articles = []

    page = 0
    print('Loading ' + city['name'])
    while (True and len(articles)<=200):
        # load next page
        page += 1
        time.sleep(1)
        url = baseUrl + str(city['id']) + '/seite/' + str(page)
        print(url)

        filePath = basePath + str(city['id']) + '-' + city['urlpart'] + '.json'
        r = requests.get(url, {})
        data: dict = r.json()

        articles = extract_articles(data, threeMonthsAgo, 50, articles)
        created = get_first_created(data)
        if (len(articles)>50) or (created < threeMonthsAgo):
            print('found ' + str(len(articles)) + ' articles since ' + threeMonthsAgo.isoformat())
            break

    with open(filePath, 'w') as outfile:
        json.dump(articles, outfile)
        print(filePath)

