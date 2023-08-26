from pymongo import MongoClient
from config import config
import logging.handlers
import sys

class MongoDatabase(object):
     def __init__(self):
          try:
               self.client = MongoClient(config["db"]["url"])  # configure db url
               self.db = self.client[config["db"]["name"]] # configure db name
               logging.info("MongoDB - Connection established")
          except Exception as e:
               logging.error("MongoDB - Connection failed")

     def insert(self, dict):
          logging.info(dict)
          try:
               inserted = self.db["fileInfo"].insert_one(dict) # insert data to db
               logging.info("MongoDB - Inserted to the MongoDB")
          except Exception as e:
               logging.error("MongoDB - Unable to insert")
               logging.error(e)
          return str(inserted.inserted_id)

     def find(self, clientId, cursor=False):  # find all from db
         try:
               found = self.db["fileInfo"].find({ "clientId": str(clientId) })
               logging.info("Client Id")
               logging.info(clientId)
               logging.info("Client history response from MongoDb")
               logging.info(found)
               found = list(found)
               for i in range(len(found)):  # to serialize object id need to convert string
                    if "_id" in found[i]:
                         found[i]["_id"] = str(found[i]["_id"])
               logging.info("Client History")
               logging.info(found)
               logging.info("MongoDB - Got Client History")
         except Exception as e:
                logging.error("MongoDB - Unable to get Client History")
         return found

