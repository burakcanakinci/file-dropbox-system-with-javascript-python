import pytest
import sys
import pika
sys.path.append('../')

from src.file_uploader.rabbitmq import RabbitMQManager  # NOQA

test_rabbitmq_config = {"user": "guest",
                        "password": "guest",
                        "host": "127.0.0.1",
                        "port": "5672",
                        "connection_timeout_s": 1200,
                        "idle_connection_timeout_s": 1800,
                        "connection_retry_s": 3,
                        "connection_retry_attempts": 5,
                        "queue_name": "test"}


def test_publish():
    """
    success
    """
    queue = RabbitMQManager(test_rabbitmq_config)
    message = "Hello World"
    result = queue.publish(message)
    assert result["message_published"] == True

    msg_received = []
    start_test_consumer(msg_received)
    assert msg_received[0] == message
    queue.shutdown_queue()


def receive_msg_wrapper(msg_received, chan):
    def receive_msg(ch, method, properties, body):
        msg_received.append(body.decode('utf-8'))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        chan.stop_consuming()
    return receive_msg


def start_test_consumer(msg_received):
    amqp_url = "amqp://{}:{}@{}:{}?connection_attempts=10&retry_delay=10".format(test_rabbitmq_config["user"],
                                                                                 test_rabbitmq_config["password"],
                                                                                 test_rabbitmq_config["host"],
                                                                                 test_rabbitmq_config["port"])
    url_params = pika.URLParameters(amqp_url)
    connection = pika.BlockingConnection(url_params)
    chan = connection.channel()

    chan.queue_declare(queue=test_rabbitmq_config["queue_name"], durable=True)
    chan.basic_qos(prefetch_count=1)
    chan.basic_consume(queue=test_rabbitmq_config["queue_name"],
                       on_message_callback=receive_msg_wrapper(msg_received, chan))

    chan.start_consuming()
