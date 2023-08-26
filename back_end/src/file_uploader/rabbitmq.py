import pika
import sys
from src.file_uploader import logger
# import logger


class RabbitMQManager:
    def __init__(self, rabbitmq_config):
        self.config = rabbitmq_config
        self.connection = self.__get_connection()
        self.queue_name = self.config["queue_name"]
        self.__init_queue()

    def __get_connection(self):
        try:
            credentials = pika.credentials.PlainCredentials(
                username=self.config["user"], password=self.config["password"])

            params = pika.connection.ConnectionParameters(
                host=self.config["host"],
                port=self.config["port"],
                credentials=credentials,
                heartbeat=self.config["connection_timeout_s"],
                blocked_connection_timeout=self.config["idle_connection_timeout_s"],
                retry_delay=self.config["connection_retry_s"],
                connection_attempts=self.config["connection_retry_attempts"])

            connection = pika.BlockingConnection(params)
            logger.log_rabbitmq_connection_success()
        except Exception as err:
            error_str = "Error while connecting to rabbitmq : " + str(err)
            logger.log_rabbitmq_connection_error(error_str)
            sys.exit(error_str)
        else:
            return connection

    def __init_queue(self):
        try:
            chan = self.connection.channel()
            chan.queue_declare(queue=self.queue_name, durable=True)
        except Exception as err:
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
            err_str = "Error while publishing message to queue : " + \
                self.queue_name + " : " + str(err)
            return {"message_published": False,
                    "error": err_str}
        else:
            return {"message_published": True}
        finally:
            if chan is not None:
                chan.close()
