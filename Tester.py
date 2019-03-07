import tweepy
import csv
import pandas as pd
'''OAUTH Authentication '''
consumer_key="wSicyi8GZRImxcHFEFAuZOlWM"
consumer_secret="0tjCcMfGCn6xCkxHl33PLjsVA2hL0GRFrbzK9LYyGeY0f7dUGT"
access_token="1098467931640528896-Uq90bCOijkbnl8JMu5MABP9U4I1ABi"
access_token_secret="ufvKtmVenU7xhWMlgnebRD2rEQIJlhLCOyIbhVF9D4N1z"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
# Open/Create a file to append data
csvFile = open('ua.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

places = api.geo_search(query="USA", granularity="country")

for place in places:
    print("placeid:%s" % place)
public_tweets = tweepy.Cursor(api.search, count=100,q="place:%s" % place.id,since="2018-06-09",show_user = True,tweet_mode="extended").items()
for tweet in public_tweets:
    print(tweet.full_text)