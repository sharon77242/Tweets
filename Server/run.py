#!/usr/bin/python3

from multiprocessing import Process
import time
from server_connection import open_server_connection
from tweets_miner import mine_tweets
from constants import COUNTRIES
from tweets_receiver import run_tweets_receiver
from tweets_file_receiver import run_tweets_file_receiver
from multiprocessing import Queue

if __name__ == "__main__":
    cycle_time = 60 * 60 * 1

    try:
        Process(target=open_server_connection, args=(), name='open_server_connection').start()
        Process(target=mine_tweets, args=(), name='mine_tweets').start()
        for country in COUNTRIES:
            try:
                time.sleep(2)
                queue = Queue()
                Process(target=run_tweets_receiver, args=(country, cycle_time, queue,),
                        name=country + ' run_tweets_receiver').start()
                Process(target=run_tweets_file_receiver, args=(queue,),
                        name=country + ' run_tweets_file_receiver').start()
            except (KeyboardInterrupt, SystemExit):
                print('Process of Country:' + country + ' Exit')
    except (KeyboardInterrupt, SystemExit):
        print('Exiting....')
