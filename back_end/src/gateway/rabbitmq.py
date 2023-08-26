import pika
import sys
import json


class RabbitMQManager:
    def __init__(self, rabbitmq_config):
        self.connection = self.__get_connection(rabbitmq_config)
        self.chan = self.connection.channel()
        self.queue_name = rabbitmq_config["queue_name"]
        self.__init_queue()

    def __get_connection(self, rabbitmq_config):
        try:
            credentials = pika.credentials.PlainCredentials(
                username=rabbitmq_config["user"], password=rabbitmq_config["password"])

            params = pika.connection.ConnectionParameters(
                host=rabbitmq_config["host"],
                port=rabbitmq_config["port"],
                credentials=credentials,
                heartbeat=rabbitmq_config["connection_timeout_s"],
                blocked_connection_timeout=rabbitmq_config["idle_connection_timeout_s"],
                retry_delay=rabbitmq_config["connection_retry_s"],
                connection_attempts=rabbitmq_config["connection_retry_attempts"])

            connection = pika.BlockingConnection(params)
        except pika.exceptions as err:
            error_str = "Error while connecting to rabbitmq : " + str(err)
            sys.exit(error_str)
        else:
            return connection

    def __init_queue(self):
        try:
            chan = self.connection.channel()
            chan.queue_declare(queue=self.queue_name, durable=True)
        except pika.exceptions as err:
            error_str = "Error while creating queue : " + str(err)
            sys.exit(error_str)
        else:
            return

    def shutdown_queue(self):
        chan = self.connection.channel()
        chan.close()
        self.connection.close()
        return

    def publish(self, message_body):
        chan = None
        try:
            if not self.connection or self.connection.is_closed:
                self.connection = self.__get_connection()
                self.__init_queue()

            chan = self.connection.channel()
            chan.basic_publish(exchange='', routing_key=self.queue_name,
                               body=message_body, properties=pika.BasicProperties(delivery_mode=2))
        except Exception as err:
            error_str = "Error while creating queue : " + str(err)
            sys.exit(error_str)
        else:
            return {"message_published": True}
        finally:
            if chan is not None:
                chan.close()

    def receive_msg(self, ch, method, properties, body):
        # msg_json = body.decode('utf-8')
        # msg = json.loads(msg_json)
        # print(msg)
        # key = msg["file_cache_key"]
        # print(" [x] Received %r" % body)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        return body
