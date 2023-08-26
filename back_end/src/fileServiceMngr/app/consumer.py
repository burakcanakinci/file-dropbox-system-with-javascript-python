import pika
import sys
import json
import service
import utils
import logging
import requests
import io
import os
from config import config
import logging.handlers
# logging.basicConfig(filename=config["logging"]["file_path"], filemode="a+", format='%(asctime)s %(levelname)s-%(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')

INSIDE_CONTAINER = os.environ.get('IN_CONTAINER_FLAG', False)

serv = service.service()


class RabbitMQManager:
    def __init__(self):
        # self.connection_url = self.__get_connection_url()
        self.connection = self.__get_connection()
        self.chan = self.connection.channel()
        self.queue_name = config["rabbitmq_config"]["queue_name"]
        self.chan.queue_declare(queue=self.queue_name, durable=True)

    # def __get_connection_url(self):
    #     return "amqp://{}:{}@{}:{}?connection_attempts=10&retry_delay=10".format(config["rabbitmq_config"]["user"],
    #                                                                              config["rabbitmq_config"]["password"],
    #                                                                              config["rabbitmq_config"]["host"],
    #                                                                              config["rabbitmq_config"]["port"],
    #                                                                              )

    def __get_connection(self):
        try:
            credentials = pika.credentials.PlainCredentials(
                username=config["rabbitmq_config"]["user"], password=config["rabbitmq_config"]["password"])

            params = pika.connection.ConnectionParameters(
                host=config["rabbitmq_config"]["host"],
                port=config["rabbitmq_config"]["port"],
                credentials=credentials,
                heartbeat=config["rabbitmq_config"]["connection_timeout_s"],
                blocked_connection_timeout=config["rabbitmq_config"]["idle_connection_timeout_s"],
                retry_delay=config["rabbitmq_config"]["connection_retry_s"],
                connection_attempts=config["rabbitmq_config"]["connection_retry_attempts"])

            connection = pika.BlockingConnection(params)
        except Exception as err:
            error_str = "Error while creating queue : " + str(err)
            sys.exit(error_str)
        else:
            return connection

    def receive_msg(self, ch, method, properties, body):
        msg_json = body.decode('utf-8')
        msg = json.loads(msg_json)
        logging.info("Obj received from rabbitMq")
        logging.info(msg)
        key = msg["file_cache_key"]
        file_contents = serv.redis_client.get(key)
        # logging.info(file_contents)
        if not file_contents['success']:
            logging.error(file_contents['error'])

        # print(file_contents)
        # file = io.BytesIO(bytes(file_contents["value"]))
        try:
            ob_id = serv.gridfs_client.insert(
                file_contents["value"], msg["file_name"])
            req_obj = utils.create_mongoDb_insert_obj(msg, ob_id)
            logging.info("Dict to be stored in MongoDb")
            logging.info(req_obj)
            inserted_id = serv.mongo_client.create(req_obj)
            logging.info("File Uploaded Successfully")
            headers, data = utils.create_fileUpload_request(
                "uploaded_successfully", msg["file_name"], msg['user_id'], msg['user_name'])
            if INSIDE_CONTAINER:
                try:
                    response = requests.put(
                        'http://file-uploader:3500/file/update/status', headers=headers, data=data)
                except requests.exceptions.ConnectionError as e:
                    print("CONNECTION ERROR: ")
                    print(e)
                    response = False

            else:
                try:
                    response = requests.put(
                        'http://localhost:3500/file/update/status', headers=headers, data=data)
                except requests.exceptions.ConnectionError as e:
                    print("CONNECTION ERROR: ")
                    print(e)
                    response = False
            if response:
                logging.info("Consumer Task Completed")
            else:
                logging.error("Consumer Task Failed")
        except Exception as e:
            logging.error(e)
            headers, data = utils.create_fileUpload_request(
                "upload_failed", msg["file_name"], msg['user_id'], msg['user_name'])
            if INSIDE_CONTAINER:
                response = requests.put(
                    'http://file-uploader:3500/file/update/status', headers=headers, data=data)
            else:
                response = requests.put(
                    'http://localhost:3500/file/update/status', headers=headers, data=data)

            # print(response.body)
            # sys.exit(error_str)
        ch.basic_ack(delivery_tag=method.delivery_tag)
