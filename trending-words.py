from config import filePaths
from config import get_cache_path
import json
import datetime
import array

with open(filePaths['cities'], 'r', encoding='utf8') as file:
    cities = json.load(file)

words = dict()
processed_ids = []
for city in cities['data']:
    filePath = get_cache_path(city)

    with open(filePath) as cityFile:
        cityData = json.load(cityFile)
        for article in cityData:
            if article['id'] in processed_ids:
                continue
            processed_ids.append(article['id'])
            article_words = article['keywords']
            #article_words = article['title'].split()
            #article_words = article['text'].split()
            created = article['dc']['created'][:10]
            week = datetime.datetime.strptime(created, '%Y-%m-%d').isocalendar()[1]
            if week not in words.keys():
                words[week] = {}

            for article_word in article_words:
                article_word = article_word.replace(':', '')
                article_word = article_word.replace('«', '')
                article_word = article_word.replace('»', '')
                article_word = article_word.replace('<p>', '')
                if article_word in words[week].keys():
                    words[week][article_word] += 1
                else:
                    words[week][article_word] = 1

last_week_words = dict()
for week in reversed(list(words.keys())):
    print('')
    print('Week: ', week)
    print('-----------')
    week_words = words[week]
    week_words = sorted(week_words.items(), key=lambda kv: kv[1])
    week_words.reverse()
    week_words = dict(week_words)

    print('Absolute:')
    i = 0
    for word in week_words:
        amount = week_words[word]
        print(word, ': ', amount)
        i+=1
        if i >= 4:
            break

    words_by_increase = {}
    for word in week_words:
        amount = week_words[word]
        if word in last_week_words and (last_week_words[word]) > 0:
            increase = week_words[word]/(last_week_words[word])
            words_by_increase[word] = increase
 
    words_by_increase = sorted(words_by_increase.items(), key=lambda kv: kv[1])
    words_by_increase.reverse()
    words_by_increase = words_by_increase[:5]
    words_by_increase = dict(words_by_increase)

    print('trending:')
    for word in words_by_increase.keys():
        rounded = round(words_by_increase[word], 2)
        print(word, ': ', rounded)

    last_week_words = week_words
