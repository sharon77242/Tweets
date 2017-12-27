from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import re
import datetime
from http.client import IncompleteRead
import time

# Twitter API credentials
consumer_key = "zBlIrsX4n5c1Z43FxsKFGJITY"
consumer_secret = "s4NniXqLAbjTtDdPKBvRtDPTUbvRSScX7UvXqLNKRAHQrPingc"
access_key = "931836587142537216-hjJ0SkbYLM8HjZRmY5gaTycaBEHfUB4"
access_secret = "zbhC62mh7mR9ioilqinajIHE2lXJ0dpNfI1YYZuC1jav7"

locations_new_york = ['NYC', ' NY', "NEW YORK"]

text = 'text'
user = 'user'
location = 'location'
place = 'place'
full_name = 'full_name'
tweets = 'TWEETS'
t_end = ''


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
        # print('original tweet:', self._tweet)
        self._tweet = self.remove_garbage(self._tweet)
        # print('after garbage remove:', self._tweet)
        # print('')
        self._file.write(self._tweet + '\n')

    def location_exists(self, curr_location):
        if self._locations[0] in curr_location or \
                self._locations[1] in curr_location or \
                self._locations[2] in curr_location.upper():
            return True
        return False

    def handle_tweet(self, data):
        all_data = json.loads(data)
        if text in all_data:
            self._tweet = all_data[text]
            if all_data[user] and all_data[user][location]:
                user_location = all_data[user][location]
                if self.location_exists(user_location):
                    # print ('user_location:', user_location)
                    self.write_tweet_to_file()

            elif all_data[place] and all_data[place][full_name]:
                curr_location = all_data[place][full_name]
                if self.location_exists(curr_location):
                    # print('curr_location:', location)
                    self.write_tweet_to_file()

    def on_data(self, data):
        if time.time() < t_end:
            self.handle_tweet(data)
            return True
        return False

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    date = datetime.datetime.now().strftime("%Y_%m_%d %H %M %S")
    t_end = time.time() + 60 * 60
    with open(tweets + ' ' + locations_new_york[2] + ' ' + date + '.txt', 'a', encoding='utf-8') as file:
        while time.time() < t_end:
            try:
                twitterStream = Stream(auth, Listener(file, locations_new_york))
                twitterStream.filter(languages=["en"], locations=[-180, -90, 180, 90])
            except IncompleteRead:
                # Oh well, reconnect and keep trucking
                continue
            except KeyboardInterrupt:
                # Or however you want to exit this loop
                twitterStream.disconnect()
                break
