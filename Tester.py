from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import json
import csv
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

'''OAUTH Authentication '''
consumer_key = config['twitter']['API']
consumer_secret = config['twitter']['APISecret']
access_token = config['twitter']['AccessToken']
access_token_secret = config['twitter']['AccessTokenSecret']

auth1 = OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token, access_token_secret)
api = API(auth1, wait_on_rate_limit=True)

print(api.me().name)
# Open/Create a file to append data
csvFile = open('tweets_id.csv', 'a', newline='')
# Use csv Writer
csvWriter = csv.writer(csvFile)


# set up stream listener
class TwitterStreamListener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        # Collect timestamp and text, filter retweets
        if ('retweeted_status' not in all_data) and ('text' in all_data):
            if 'extended_tweet' in all_data:  # Handle tweets >140 chars
                ext = all_data['extended_tweet']
                tweet = ext['full_text']
            else:
                tweet = all_data['text']
            tweet_id = all_data['id']
            created_at = all_data['created_at']
            print(tweet_id, created_at, tweet)
            csvWriter.writerow([tweet_id, created_at, tweet.encode("utf-8")])

    def on_error(self, status):
        print(status)


track = ['democrat', 'republican', 'trump', 'president', 'potus', 'congress', 'supreme court', 'scotus',
         'candidate', 'nomination', 'nominee', 'legislat', 'politic']

# create stream and filter on a terms listed above
twitterStream = Stream(auth1, TwitterStreamListener())
twitterStream.filter(track=track, languages=["en"], stall_warnings=True)