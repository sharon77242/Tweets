#!/usr/bin/python
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import re
import datetime
from http.client import IncompleteRead
import time

# Twitter API credentials
c_consumer_key = "zBlIrsX4n5c1Z43FxsKFGJITY"
c_consumer_secret = "s4NniXqLAbjTtDdPKBvRtDPTUbvRSScX7UvXqLNKRAHQrPingc"
c_access_key = "931836587142537216-hjJ0SkbYLM8HjZRmY5gaTycaBEHfUB4"
c_access_secret = "zbhC62mh7mR9ioilqinajIHE2lXJ0dpNfI1YYZuC1jav7"

c_new_york = 'new york'
c_locations_new_york = [c_new_york, 'nyc', ' ny']

c_los_angeles = 'los angeles'
c_locations_los_angeles = [c_los_angeles, ', la']

c_california = 'california'
c_locations_california = [c_california, ', ca ']

current_location = c_locations_california

c_text = 'text'
c_user = 'user'
c_location = 'location'
c_place = 'place'
c_full_name = 'full_name'
c_tweets = 'tweets'
time_end = ''
c_txts = 'txts'


class Listener(StreamListener):

    def __init__(self, file, locations):
        StreamListener.__init__(self)
        self._file = file
        self._locations = locations
        self._tweet = ''

    @staticmethod
    def remove_garbage(tweet):
        tweet = tweet.replace('\r', '').replace('\n', ' ')              # remove \r and \n
        tweet = json.dumps(tweet, ensure_ascii=False)                   # convert tweet to text
        tweet += '\n'                                                   # add new line to remove url's on end of row
        tweet = re.sub(r'http.*? ', ' ', tweet, flags=re.IGNORECASE)    # remove url's ending with space ' '
        tweet = re.sub(r'http.*?\r', ' ', tweet, flags=re.IGNORECASE)   # remove url's ending with \r
        tweet = re.sub(r'http.*?\n', ' ', tweet, flags=re.IGNORECASE)   # remove url's ending with \n
        tweet = re.sub(r'\s+', ' ', tweet)                              # eliminate duplicate spaces
        tweet = tweet.replace('"', '')                                  # remove "" from strings

        return tweet

    def write_tweet_to_file(self):
        print('original tweet:', self._tweet)
        self._tweet = self.remove_garbage(self._tweet)
        print('after garbage remove:', self._tweet)
        print('')
        self._file.write(self._tweet + '\n')

    def location_exists(self, curr_location):
        for location in self._locations:
            if location in curr_location :
                return True
        return False

    def handle_tweet(self, data):
        all_data = json.loads(data)
        if c_text in all_data:
            if all_data[c_user] and all_data[c_user][c_location]:
                user_location = all_data[c_user][c_location].lower()
                if self.location_exists(user_location):
                    print('user_location:', user_location)
                    self._tweet = all_data[c_text]
                    self.write_tweet_to_file()

            elif all_data[c_place] and all_data[c_place][c_full_name]:
                curr_location = all_data[c_place][c_full_name].lower()
                if self.location_exists(curr_location):
                    print('curr_location:', curr_location)
                    self._tweet = all_data[c_text]
                    self.write_tweet_to_file()

    def on_data(self, data):
        if time.time() < time_end:
            self.handle_tweet(data)
            return True
        return False

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    auth = OAuthHandler(c_consumer_key, c_consumer_secret)
    auth.set_access_token(c_access_key, c_access_secret)

    date = datetime.datetime.now().strftime("%Y_%m_%d %H %M %S")
    time_end = time.time() + 60 * 120

    file_name = c_txts + '/' + c_tweets + ' ' + current_location[0] + ' ' + date + '.txt'

    with open(file_name, 'a', encoding='utf-8') as file:
        while time.time() < time_end:
            try:
                twitterStream = Stream(auth, Listener(file, current_location))
                twitterStream.filter(languages=["en"], locations=[-180, -90, 180, 90])
            except IncompleteRead:
                # Oh well, reconnect and keep trucking
                continue
            except KeyboardInterrupt:
                # Or however you want to exit this loop
                twitterStream.disconnect()
                break
