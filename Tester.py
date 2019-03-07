from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import json
import csv
'''OAUTH Authentication '''
consumer_key="wSicyi8GZRImxcHFEFAuZOlWM"
consumer_secret="0tjCcMfGCn6xCkxHl33PLjsVA2hL0GRFrbzK9LYyGeY0f7dUGT"
access_token="1098467931640528896-Uq90bCOijkbnl8JMu5MABP9U4I1ABi"
access_token_secret="ufvKtmVenU7xhWMlgnebRD2rEQIJlhLCOyIbhVF9D4N1z"

auth1 = OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token, access_token_secret)
api = API(auth1, wait_on_rate_limit=True)

print(api.me().name)
# Open/Create a file to append data
csvFile = open('tweets.csv', 'a', newline='')
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
            created_at = all_data['created_at']
            print(created_at, tweet)
            csvWriter.writerow([created_at, tweet.encode("utf-8")])

    def on_error(self, status):
        print(status)


track = ['democrat', 'republican', 'trump', 'president', 'potus', 'congress', 'supreme court', 'scotus',
         'candidate', 'nomination', 'nominee', 'legislat', 'politic']

# create stream and filter on a terms listed above
twitterStream = Stream(auth1, TwitterStreamListener())
twitterStream.filter(track=track, languages=["en"], stall_warnings=True)