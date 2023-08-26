import pymongo
#
# client = pymongo.MongoClient("mongodb://:27017/")
#
# db = client["test_database"]
#
# courses = db["course"]
#
#
# dict = {"name":"Shubham","activity":"test"}
#
#
# x = courses.insert_one(dict)
# print(x)

# import boto3
# import os
#
# client = boto3.client('s3',
#                         aws_access_key_id = "AKIA5UVQCCOP2IPAQU5J",
#                         aws_secret_access_key = "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")
#
#
# file = open('saveimg_h50_w50_score1_search20.jpg','rb')
# upload_file_bucket = 'weightsbucket'
# upload_file_key = 'weights/' + str(file)
# print(upload_file_key)
# client.upload_fileobj(file, upload_file_bucket, str(upload_file_key))


# logging.basicConfig(filename="/logs/logFile.txt",filemode="a+",format='%(asctime)s %(levelname)s-%(message)s',
#                      datefmt='%Y-%m-%d %H:%M:%S')
#
#
# app = Flask(__name__)
#redis = redis.Redis(host='redis', port=6379, db=0)
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
# @app.route('/visitor')
# def visitor():
#     #redis.incr('visitor')
#     #visitor_num = redis.get('visitor').decode("utf-8")
#     logging.warning('visitor API')
#     return "Visitor: %s" % (1)
# @app.route('/visitor/reset')
# def reset_visitor():
#     #redis.set('visitor', 0)
#     #visitor_num = redis.get('visitor').decode("utf-8")
#     logging.warning('Reset API')
#     return "Visitor is reset to %s" % (2)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')


# @app.route('/client/history/<client_id>', methods=['GET'])
# def getClientHistory(client_id) -> str:
#     clientId = client_id
#     return json.dumps({'client_history': clients_history(clientId)})
#
# @app.route('/file/upload', methods=['GET','POST'])
# def fileUpload():
#     if request.method == 'POST':
#         if request.files:
#            file = request.files["file"]
#            print("Request form",file=sys.stderr)
#            app.logger.info(request.form)
#            id,col = update_col(request.form,file,mongo)
#            succ = update_client_history(request.form,id,file.filename)
#            return json.dumps({"filename": file.filename, "mongo_db_id":str(id)})
#     return make_response(jsonify(success=False))


# @app.route('/client/list',methods=['GET'])
# def lstfiles():
#     return json.dumps({'files':list_files()})


# @app.route('/clients/update/<client_id>', methods=['GET','POST'])
# def updateClientHistory(client_id) -> str:
#     if request.method == 'POST':
#         clientId = client_id
#         req_data = request.json
#         succ=update_client_history(clientId,req_data)
#         return make_response(jsonify(success=succ))
#     return make_response(jsonify(success=False))


from pymongo import MongoClient
from gridfs import GridFS
from bson import objectid
import service
serv = service.service()

db = MongoClient("mongodb://127.0.0.1:27017/").mygrid

fs = GridFS(db,"stringfiles")


ob_id = serv.gridfs_client.insert("absas","test4.txt")
#f_id =serv.gridfs_client.db.files.find_one({ "filename" : "test3.txt" },{ "_id" : 1 })

print(serv.gridfs_client.search("test4.txt"))

# ob = fs.put("hello worldasas", encoding='utf-8',filename='test1.txt')
#
# f_id = db.stringfiles.files.find_one({ "filename" : "test1.txt" },{ "_id" : 1 })
#
# print(type(ob))
# print(fs.get(f_id['_id']).read())


#print(fs.get(ob).read())

'''
from flask import Flask, request, jsonify, make_response
from config import config
import logging
import os
from time import sleep

import logging.handlers


logger = logging.getLogger()
fh = logging.handlers.RotatingFileHandler(filename=config["logging"]["file_path"], maxBytes=10240, backupCount=5)
#fh.setLevel(logging.DEBUG)#no matter what level I set here
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.setLevel(logging.DEBUG)

app = Flask(__name__)
ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", False)
ENVIRONMENT_PORT = os.environ.get("APP_PORT", 6000)
logging.info("HAHA")
logging.debug("It is working finally using config --- also from outside")
logging.info("Project has started")
app.run(host='0.0.0.0', port=ENVIRONMENT_PORT,
        debug=ENVIRONMENT_DEBUG, use_reloader=False, passthrough_errors=True)
logging.info("After app run")
'''
#logging.getLogger().addHandler(logging.StreamHandler())

# while(1):
#     logging.info(config["logging"]["file_path"])
#     logging.info("Started")
#     print("Project started")
#     sleep(10)