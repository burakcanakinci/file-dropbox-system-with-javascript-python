from redis import RedisError, sentinel
import sys

ERROR_KEY_NOT_FOUND = "Key not found in redis"


class RedisDriver:
    def __init__(self, redis_config):
        self.service = redis_config["service_name"]
        self.__connect(redis_config)

    def __connect(self, redis_config):
        try:
            self.connection = sentinel.Sentinel([(redis_config["master_host"],
                                                  redis_config["master_port"]),
                                                 (redis_config["slave_1_host"],
                                                  redis_config["slave_1_port"]),
                                                 (redis_config["slave_2_host"],
                                                  redis_config["slave_2_port"]),
                                                 (redis_config["slave_3_host"],
                                                  redis_config["slave_3_port"])],
                                                min_other_sentinels=2,
                                                encoding="utf-8",
                                                decode_responses=True)

        except RedisError as err:
            error_str = "Error while connecting to redis : " + str(err)
            sys.exit(error_str)

    def set(self, key, value):
        key_str = str(key)
        val_str = str(value)
        try:
            master = self.connection.master_for(self.service)
            master.set(key_str, val_str)
            return {"success": True}
        except RedisError as err:
            error_str = "Error while connecting to redis : " + str(err)
            return {"success": False,
                    "error": error_str}

    def get(self, key):
        key_str = str(key)
        try:
            master = self.connection.master_for(self.service)
            value = master.get(key_str)
        except RedisError as err:
            error_str = "Error while retrieving value from redis : " + str(err)
            return {"success": False,
                    "error": error_str}

        if value is not None:
            return {"success": True,
                    "value": value}
        else:
            return {"success": False,
                    "error": ERROR_KEY_NOT_FOUND}

    def delete(self, key):
        key_str = str(key)
        try:
            master = self.connection.master_for(self.service)
            value = master.delete(key_str)
        except RedisError as err:
            error_str = "Error while deleting key from redis : " + str(err)
            return {"success": False,
                    "error": error_str}

        return {"success": True}
