import pika
from urllib3.exceptions import ProtocolError
from constants import COUNTRIES
from constants import TWEETS
from constants import URL


def get_rabbit_mq_connection():
    try:
        parameters = pika.ConnectionParameters(URL)
        return pika.BlockingConnection(parameters)
    except Exception as e:
        print(e)
        raise e


def connect_to_rabbit_mq():
    try:
        connection = get_rabbit_mq_connection()
        channel = connection.channel()
        for country in COUNTRIES:
            channel.queue_declare(queue=country + " " + TWEETS)
            channel.queue_declare(queue=country + " " + TWEETS + " file")
        return channel
    except ProtocolError as ex:
        channel.close()
        print("ERROR : connections closed: " + ex)
    except KeyboardInterrupt:
        channel.close()
