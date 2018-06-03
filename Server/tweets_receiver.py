from rabit_mq_connection import connect_to_rabbit_mq
from tweets_file_creator import FileCreator
from constants import TWEETS

file_creator = None


def callback(ch, method, properties, body):
    text = str(body, encoding="utf-8")
    # print(" [x] Received tweet %r" % text)
    file_creator.country_tweets_file.write(text + '\n')
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_tweets_receiver(country, cycle_time, queue):
    channel = connect_to_rabbit_mq()
    global file_creator
    file_creator = FileCreator(channel, country, cycle_time, queue)
    channel.basic_consume(callback, queue=country + ' ' + TWEETS)
    channel.start_consuming()
