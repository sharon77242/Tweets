import json
import re
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from constants import *


class Listener(StreamListener):

    def __init__(self, locations, channel):
        StreamListener.__init__(self)
        self._locations = locations
        self._tweet = ''
        self._channel = channel

    def on_data(self, data):
        self.handle_tweet(data)
        return True

    def on_error(self, status):
        print('ERROR: with status ' + str(status))

    def remove_garbage(self, tweet):
        tweet = tweet.replace('\r', '').replace('\n', ' ')  # remove \r and \n
        tweet = json.dumps(tweet, ensure_ascii=False)  # convert tweet to text
        tweet += '\n'  # add new line to remove url's on end of row
        tweet = re.sub(r'http.*? ', ' ', tweet, flags=re.IGNORECASE)  # remove url's ending with space ' '
        tweet = re.sub(r'http.*?\r', ' ', tweet, flags=re.IGNORECASE)  # remove url's ending with \r
        tweet = re.sub(r'http.*?\n', ' ', tweet, flags=re.IGNORECASE)  # remove url's ending with \n
        tweet = re.sub(r'\s+', ' ', tweet)  # eliminate duplicate spaces
        tweet = tweet.replace('"', '')  # remove "" from strings

        return tweet

    def write_tweet_to_file(self, country):
        #print('original tweet:', self._tweet)
        self._tweet = self.remove_garbage(self._tweet)
        # print('after garbage remove:', self._tweet)
        # print('')
        self._channel.basic_publish(exchange='', routing_key=country + ' ' + TWEETS, body=self._tweet)
        # self._file.write(self._tweet + '\n')

    def location_exists(self, curr_location):
        for location in self._locations:
            if location in curr_location:
                return (True, COUNTRIES_DICT.get(location))
        return (False, None)

    def handle_tweet(self, data):
        all_data = json.loads(data)
        if TEXT in all_data:
            if all_data[USER] and all_data[USER][LOCATION]:
                user_location = all_data[USER][LOCATION].lower()
                exists, country_name = self.location_exists(user_location)
                if exists:
                    # print('user_location:', user_location)
                    self._tweet = all_data[TEXT]
                    self.write_tweet_to_file(country_name)

            elif all_data[PLACE] and all_data[PLACE][FULL_NAME]:
                curr_location = all_data[PLACE][FULL_NAME].lower()
                exists, country_name = self.location_exists(curr_location)
                if exists:
                    # print('curr_location:', curr_location)
                    self._tweet = all_data[TEXT]
                    self.write_tweet_to_file(country_name)


def create_twitter_stream(rabbit_filter, channel):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return Stream(auth, Listener(rabbit_filter, channel))
