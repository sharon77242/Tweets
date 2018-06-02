import rabit_mq_connection
from model_manager import run_model_stage


def callback(ch, method, properties, body):
    print('writeBestTweetToFile::callback')

    tweets_file = str(body, encoding="utf-8")
    print(" [x] Received tweets file %r" % tweets_file)

    run_model_stage(tweets_file)


def run_tweets_file_receiver(country):
    channel = rabit_mq_connection.connect_to_rabbit_mq()
    channel.basic_consume(callback, queue=country + ' tweets file', no_ack=True)
    channel.start_consuming()
