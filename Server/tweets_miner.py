#!/usr/bin/python

import rabit_mq_connection
from urllib3.exceptions import ProtocolError
from tweets_listener import create_twitter_stream
from constants import COUNTRIES_FILTER


def mine_tweets():
    channel = rabit_mq_connection.connect_to_rabbit_mq()
    twitter_stream = create_twitter_stream(COUNTRIES_FILTER, channel)
    try:
        twitter_stream.filter(languages=["en"], locations=[-180, -90, 180, 90])
    except ProtocolError as ex:
        twitter_stream.disconnect()
        channel.close()
        print("ERROR :connection closed: " + ex)
    except KeyboardInterrupt:
        twitter_stream.disconnect()
        channel.close()
