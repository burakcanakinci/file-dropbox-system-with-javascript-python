from models import models, redis_model, gridFs_model
from models import redis_model
from config import config
import boto3

class service:
    def __init__(self):
        self.mongo_client = self.getMongoDbModel()
        self.redis_client = self.getRedisModel()
        self.aws_client = self.getAwsModel()
        self.gridfs_client = self.getGridfsClient()
        return

    def getMongoDbModel(self):
        return models.model()

    def getRedisModel(self):
        return redis_model.RedisDriver(config["index_cache_config"])

    def getAwsModel(self):
        return boto3.client('s3', aws_access_key_id=config["aws"]["access_key"], aws_secret_access_key=config["aws"]["secret_access_key"])

    def getGridfsClient(self):
        return gridFs_model.model()


