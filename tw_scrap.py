#!/usr/bin/env python

"""
Use Twitter API to grab user information from list of organizations;
export text file
Uses Twython module to access Twitter API
"""

import sys
import string
import simplejson
from twython import Twython
import pandas as pd

from django.utils.encoding import smart_str, smart_unicode

import datetime

import pytz




now = datetime.datetime.now()
day = int(now.day)
month = int(now.month)
year = int(now.year)

# FOR OAUTH AUTHENTICATION -- NEEDED TO ACCESS THE TWITTER API
t = Twython(app_key='sHAzl0KXJQat8NeUsR3CTWvMv',
            app_secret='xXR4OTuAvu9c8TbOiTvqEg1G5MKqjst0p9Yx2vEdWur87kvTL8',
            oauth_token='852360084-w0bcCcThGPvdC4DjzWjz0zSCMbamvk4wvJfsICmT',
            oauth_token_secret='9O5xHXST9xv8bBJsFk5QXp7A8rLJBvPTVkLFOHMNVOtnb')

userid = pd.read_csv("C:/Users/gowri/Documents/Yourfeed/code/Twitter/companies.csv")
userid= userid.dropna()




ids= userid['TwitterHandle'].tolist()


users = t.lookup_user(screen_name=ids)


r = []
count =0
for entry in users:
    fav=0
    retweet=0
    urls=0


    d = t.get_user_timeline(screen_name= smart_str(entry['screen_name']), count="100", include_entities="true", include_rts="1")
    for e in d:
        retweet += e['retweet_count']
        fav += e['favorite_count']
        if 'media' in e['entities']:
            urls += 1



    created_at = entry['created_at']

    s = datetime.datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
    tino = s.tzinfo

    no_days = datetime.datetime.now(tino) - s
    avg_tweets=  float(entry['statuses_count']/ no_days.days)

    if not r:
        r = [[smart_str(entry['screen_name'])] +  [smart_str(entry['name'])] +  [smart_str(entry['created_at'])] + [entry['followers_count']] +  [entry['statuses_count']] +[entry['favourites_count']] + [avg_tweets]+ [retweet] + [fav] +[urls]]
    else:
        r.append([smart_str(entry['screen_name'])] +  [smart_str(entry['name'])] +  [smart_str(entry['created_at'])] + [int(entry['followers_count'])] + [int(entry['statuses_count'])] +[int(entry['favourites_count'])] + [avg_tweets]+ [retweet] + [fav] +[urls])
    count += 1
    print count

out= pd.DataFrame(r,columns=('ScreenName','Name','Created_at','Followers','Tweet_count','Fav_count','Average_posts','Retweets_in_100', 'Fav_in_100', 'Media_100'))

out['Rank']=  (out['Followers'] *0.10) + (out['Average_posts']*0.25) + (out['Retweets_in_100'] * 0.25) + (out['Fav_in_100'] *0.25) + (out['Media_100'] * 0.15)

out= out.sort_values(by='Rank', ascending=[False])

out = out.reset_index(drop=True)


out.to_csv("C:/Users/gowri/Documents/Yourfeed/code/Twitter/twitter_companies_data.csv")

out.to_json(path_or_buf="C:/Users/gowri/Documents/Yourfeed/code/Twitter/twitter_companies_data.json", orient='index')

