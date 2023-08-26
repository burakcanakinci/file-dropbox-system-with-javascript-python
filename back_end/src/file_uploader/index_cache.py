import json
from src.file_uploader import redis_driver
# import redis_driver

STATUS_FILE_CACHED = "File stored in cache"
STATUS_FILE_UPLOADED = "File uplaoded successfully"
STATUS_RETRY_UPLOAD = "File upload failed previously. Retrying now."
STATUS_UPLOAD_FAILED = "FIle upload failed after max attempts"
ERROR_MAX_ATTEMPTS_REACHED = "File upload has been retried maximum number of times"


class IndexCache:
    def __init__(self, redis_config):
        self.redis = redis_driver.RedisDriver(redis_config)

    def create(self, file_name, meta_data):
        index_key = self.__get_key(file_name)
        value = {"status": STATUS_FILE_CACHED,
                 "metadata": meta_data,
                 "attempt": 1}
        val_json = json.dumps(value)

        result = self.redis.set(index_key, val_json)
        return result

    def update_uploaded(self, file_name):
        index_key = self.__get_key(file_name)

        result = self.__check_if_index_key_exists(index_key)
        if not result["success"]:
            return result

        value = json.loads(result["value"])
        value["status"] = STATUS_FILE_UPLOADED
        val_json = json.dumps(value)

        result = self.redis.set(index_key, val_json)
        return result

    def update_retry(self, file_name, max_attempts):
        index_key = self.__get_key(file_name)

        result = self.__check_if_index_key_exists(index_key)
        if not result["success"]:
            return result

        value = json.loads(result["value"])
        if value["attempt"] >= max_attempts:
            self.__update_upload_failed(file_name, max_attempts)
            return {"success": False,
                    "error": ERROR_MAX_ATTEMPTS_REACHED}

        value["status"] = STATUS_RETRY_UPLOAD
        value["attempt"] += 1
        val_json = json.dumps(value)

        result = self.redis.set(index_key, val_json)
        if result["success"]:
            result["metadata"] = value["metadata"]
        return result

    def __update_upload_failed(self, file_name, max_attempts):
        index_key = self.__get_key(file_name)

        value = {"status": STATUS_UPLOAD_FAILED, "attempt": max_attempts}
        val_json = json.dumps(value)

        result = self.redis.set(index_key, val_json)
        return result

    def __check_if_index_key_exists(self, file_name):
        return self.redis.get(file_name)

    def __get_key(self, file_name):
        return "file_index:" + file_name
