import datetime
import threading
from constants import TXTS
from constants import TWEETS


class FileCreator():
    def __init__(self, channel, country, cycle_time):
       #print("File Creator Started!")
        self._cycle_time = cycle_time
        self.country_tweets_file = None
        self._country = country
        self._channel = channel
        self._update_tweets_files()

    def _get_next_tweets_file_name(self):
        date = datetime.datetime.now().strftime("%Y_%m_%d %H %M %S")
        file_name = TXTS + '/' + TWEETS + ' ' + self._country + ' ' + date + '.txt'
        return open(file_name, 'a', encoding='utf-8')

    def _update_tweets_files(self):
        #print('FileCreator::_updateTweetsFiles')
        self._close_old_tweets_files()
        self.country_tweets_file = self._get_next_tweets_file_name()
        threading.Timer(self._cycle_time, self._update_tweets_files).start()

    def _close_old_tweets_files(self):
        if self.country_tweets_file is not None:
            print('FileCreator::closed old tweets file ' + self._country)
            self.country_tweets_file.close()
            self._channel.basic_publish(exchange='', routing_key=self._country + ' tweets file',
                                        body=self.country_tweets_file.name)
