#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 08:25:04 2018

@author: connorenglish
"""

import schedule
import time
import tweepy
import json
from textgenrnn import textgenrnn
import urllib.request
import random
from contextlib import redirect_stdout
import language_check
tool = language_check.LanguageTool('en-US')

# gets all of our data from the config file.
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

screen_name = config_data["auth"]["screen_name"]

# authorization from values inputted earlier, do not change.
auth = tweepy.OAuthHandler(config_data["auth"]["CONSUMER_KEY"], config_data["auth"]["CONSUMER_SECRET"])
auth.set_access_token(config_data["auth"]["ACCESS_TOKEN"], config_data["auth"]["ACCESS_SECRET"])
api = tweepy.API(auth)

turtle_model=textgenrnn(weights_path='prawn_meat_Fred_Delicious_BarackObama_twitter_weights.hdf5',
                   config_path='prawn_meat_Fred_Delicious_BarackObama_twitter_config.json',
                   vocab_path='prawn_meat_Fred_Delicious_BarackObama_twitter_vocab.json')

listononos = ['Obama','reform','JUNBC','Trump','trump','sector','President','Pence','White House','/n','Selma','Garland','Merrick',
              'fuck','ass','dick','hell','piss','shit','pubic','pussy','horny','bitch','bong','damn','government',
              '#','equal pay','Ted Cruz','climate change','vote','partisan','Climate change','American workers',
              'coverage','#GetCovered','Congress','Supreme', 'Court', 'clean energy','weekly address', 'Biden','Iran','health insurance','health care']

special_characters = ["[", "]", ":", '"']

hots = [.5]

pics = ["https://picsum.photos/500/300/?random",
        "https://picsum.photos/500/400/?random",
        "https://picsum.photos/500/500/?random",
        "https://picsum.photos/300/500/?random",
        "https://picsum.photos/200/500/?random",
        "https://picsum.photos/600/400/?random"]


def trend_tweet():
    trends1 = api.trends_place(23424977)
    data = trends1[0]
    trends = data['trends']
    names = [trend['name'] for trend in trends]
    names = names[:10]
    names = random.choice(names)
    if '#' in names:
        while True:
            with open('output.txt', 'w') as f:
                with redirect_stdout(f):
                    turtle_model.generate(n=1, temperature=random.choice(hots))
            with open('output.txt', 'r') as myfile:
                status=myfile.read()
            if (not any(x in status for x in listononos)) & (len(status) < 100):
                    break
        matches = tool.check(status)
        status = language_check.correct(status, matches)
        with open('output.txt', 'w') as f:
            with redirect_stdout(f):
                print(names, status.rstrip())
        with open('output.txt', 'r') as myfile:
            status=myfile.read()
            status = status.replace("[", "")
            status = status.replace("]", "")
            status = status.replace(":", "")
            status = status.replace('"', "")
            print(status)
            api.update_status(status)
    else:
        while True:
            with open('output.txt', 'w') as f:
                with redirect_stdout(f):
                    turtle_model.generate(n=1, temperature=random.choice(hots))
            with open('output.txt', 'r') as myfile:
                status=myfile.read()
            if (not any(x in status for x in listononos)) & (len(status) < 100):
                    break
        matches = tool.check(status)
        status = language_check.correct(status, matches)
        with open('output.txt', 'w') as f:
            with redirect_stdout(f):
                print(status.rstrip(), '-', names)
        with open('output.txt', 'r') as myfile:
            status=myfile.read()
            status = status.replace("[", "")
            status = status.replace("]", "")
            status = status.replace(":", "")
            status = status.replace('"', "")
            print(status)
            api.update_status(status)

    return

def regular_tweet():
    while True:
        with open('output.txt', 'w') as f:
            with redirect_stdout(f):
                turtle_model.generate(n=1, temperature=random.choice(hots))
        with open('output.txt', 'r') as myfile:
            status=myfile.read()
            status = status.replace("[", "")
            status = status.replace("]", "")
            status = status.replace(":", "")
            status = status.replace('"', "")
        if (not any(x in status for x in listononos)) & (len(status) < 100):
            break
    matches = tool.check(status)
    status = language_check.correct(status, matches)
    status = status.replace('Re tweet', 'Retweet')
    print(status)
    api.update_status(status)
    return

def pic_tweet():
    urllib.request.urlretrieve(random.choice(pics), "tweetpic.jpg")
    while True:
        with open('output.txt', 'w') as f:
            with redirect_stdout(f):
                turtle_model.generate(n=1, temperature=random.choice(hots))
        with open('output.txt', 'r') as myfile:
            status=myfile.read()
            status = status.replace("[", "")
            status = status.replace("]", "")
            status = status.replace(":", "")
            status = status.replace('"', "")
        if (not any(x in status for x in listononos)) & (len(status) < 100):
            break
    matches = tool.check(status)
    status = language_check.correct(status, matches)
    api.update_with_media("tweetpic.jpg", status)
    return

def pic_trend_tweet():
    trends1 = api.trends_place(23424977)
    data = trends1[0]
    trends = data['trends']
    names = [trend['name'] for trend in trends]
    names = names[:10]
    urllib.request.urlretrieve(random.choice(pics), "tweetpic.jpg")
    while True:
        with open('output.txt', 'w') as f:
            with redirect_stdout(f):
                turtle_model.generate(n=1, temperature=random.choice(hots))
        with open('output.txt', 'r') as myfile:
            status=myfile.read()
        if (not any(x in status for x in listononos)) & (len(status) < 100):
            break
    matches = tool.check(status)
    status = language_check.correct(status, matches)
    with open('output.txt', 'w') as f:
        with redirect_stdout(f):
            print(status.rstrip(), '-', random.choice(names))
    with open('output.txt', 'r') as myfile:
        status=myfile.read()
        status = status.replace("[", "")
        status = status.replace("]", "")
        status = status.replace(":", "")
        status = status.replace('"', "")
    api.update_with_media("tweetpic.jpg", status)
    return

schedule.every().day.at("8:00").do(trend_tweet)
schedule.every().day.at("9:00").do(regular_tweet)
schedule.every().day.at("10:00").do(regular_tweet)
schedule.every().day.at("11:00").do(regular_tweet)
schedule.every().day.at("12:00").do(trend_tweet)
schedule.every().day.at("13:00").do(regular_tweet)
schedule.every().day.at("14:00").do(regular_tweet)
schedule.every().day.at("15:00").do(regular_tweet)
schedule.every().day.at("16:00").do(trend_tweet)
schedule.every().day.at("17:00").do(regular_tweet)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
