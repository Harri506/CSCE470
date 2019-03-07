import sys
import tweepy
import csv
import time

'''OAUTH Authentication '''
consumer_key="wSicyi8GZRImxcHFEFAuZOlWM"
consumer_secret="0tjCcMfGCn6xCkxHl33PLjsVA2hL0GRFrbzK9LYyGeY0f7dUGT"
access_token="1098467931640528896-Uq90bCOijkbnl8JMu5MABP9U4I1ABi"
access_token_secret="ufvKtmVenU7xhWMlgnebRD2rEQIJlhLCOyIbhVF9D4N1z"

auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth1, wait_on_rate_limit=True)

print(api.me().name)
# Open/Create a file to append data
csvFile = open('tweets.csv', 'a', newline='')
# Use csv Writer
csvWriter = csv.writer(csvFile)


class StreamListenerTwitter(tweepy.StreamListener):
    def on_status(self, status):
        try:
            content = status.extended_tweet["full_text"].encode('utf-8')
            tw_time = status.created_at
            if not ('RT @'.encode('utf-8') in content):  # Exclude re-tweets
                print(tw_time, content)
                csvWriter.writerow([tw_time, content])
        except AttributeError:
            content = status.text.encode('utf-8')
            tw_time = status.created_at
            csvWriter.writerow([tw_time, content])

    def on_error(self, status_code):
        print('Error: ' + repr(status_code))
        return True  # False to stop

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        print("Delete notice for %s. %s" % (status_id, user_id))
        return

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        print("!!! Limitation notice received: %s" % str(track))
        return

    def on_timeout(self):
        print('Timeout...')
        time.sleep(10)
        return True


def main():
    track = ['democrat', 'republican', 'trump', 'president', 'potus', 'congress', 'supreme court', 'scotus',
             'candidate', 'nomination', 'nominee', 'legislat', 'politic']
    streamTube = tweepy.Stream(auth=auth1, listener=StreamListenerTwitter(), timeout=300)

    print("Streaming started...")

    try:
        streamTube.filter(track=track, languages=["en"])
        csvFile.close()
    except Exception as e:
        print("Stream error:", e)
        streamTube.disconnect()


if __name__ == '__main__':
    main()
