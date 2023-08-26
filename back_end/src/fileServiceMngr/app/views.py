from flask import Flask, request, jsonify, make_response, Response
import json
import service
import os
from config import config
import consumer
import threading
import logging
import logging.handlers
import datetime
from bson import ObjectId
app = Flask(__name__)
serv = service.service()




@app.route('/file/<filename>',methods=['GET'])
def getFile(filename) ->str:
    logging.info("Download File API")
    try:
        logging.info("File Id")
        logging.info(filename)
        file_content = serv.gridfs_client.getFile(filename)
        # file_metadata = serv.mongo_client.getMetaData(filename)
        response = make_response(eval(file_content))
        logging.info("Response created")
        logging.info(response)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers["Content-Disposition"] = "attachment; fileId={}".format(filename)
        logging.info("File Download API - sending the file")
        return response
    except Exception as e:
        logging.error("File Download API- Error in file Download")
        logging.error(e)



@app.route('/client/history/<client_id>', methods=['GET'])
def getClientHistory(client_id) -> str:
    logging.info('ClientHistory API')
    try:
        logging.info("Client Id")
        logging.info(client_id)
        clientHstry = serv.mongo_client.find(client_id)
        logging.info('Main-Client History')
        logging.info(clientHstry)
        logging.info(type(clientHstry))
        logging.info("MongoDb - Got client Historya")
        return json.dumps(clientHstry,indent=4, sort_keys=True, default=str)
    except Exception as e:
        logging.error("MongoDb - Got error on fetching data from MongoDb")
    return False

'''
/file/upload route should be removed in future. It is 
just to test FSM services independently.
'''
@app.route('/file/upload', methods=['GET', 'POST'])
def fileUpload():
    if request.method == 'POST':
        if request.files:
            logging.info('fileUpload API')
            file = request.files["file"]
            req = request.form.to_dict(flat=False)
            # upload_file_bucket = 'weightsbucket'
            upload_file_key = 'weights/' + str(file.filename)
            req["fileName"] = upload_file_key
            # req["url"] = url
            inserted_id = serv.mongo_client.create(req)
            return json.dumps({"filename": file.filename, "mongo_db_id": str(inserted_id)})
    return make_response(jsonify(success=False))

'''
All the 500 errors will be routed here
'''
@app.errorhandler(500)
def internal_error(exception):
    logging.error(exception)
    return False, 500


class ThreadedTask(threading.Thread):
    def __init__(self, ):
        threading.Thread.__init__(self)

    def run(self):
        queue_manager = consumer.RabbitMQManager()
        queue_manager.chan.basic_qos(prefetch_count=1)
        queue_manager.chan.basic_consume(queue=queue_manager.queue_name,
                                         on_message_callback=queue_manager.receive_msg)
        queue_manager.chan.start_consuming()


if __name__ == '__main__':
    logger = logging.getLogger()
    fh = logging.handlers.RotatingFileHandler(filename=config["logging"]["file_path"], maxBytes=10240, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", False)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 4500)
    task = ThreadedTask()
    task.start()
    logging.info("RabbitMq thread started")
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT,
            debug=ENVIRONMENT_DEBUG, use_reloader=False, passthrough_errors=True)
