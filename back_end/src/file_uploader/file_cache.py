from src.file_uploader import redis_driver
# import redis_driver

ERROR_FILE_NOT_FOUND = "File not found"
ERROR_EMPTY_FILE = "File is empty"


class FileCache:
    def __init__(self, redis_config):
        self.redis = redis_driver.RedisDriver(redis_config)

    def get_key(self, file_name):
        return "file:" + file_name

    def store(self, file_path, file_name):
        file = None
        try:
            file = open(file_path, 'rb')
            file_contents = file.read()
        except FileNotFoundError:
            return {"success": False,
                    "error": ERROR_FILE_NOT_FOUND}
        finally:
            if file is not None:
                file.close()

        if file_contents is None or len(file_contents) == 0:
            return {"success": False,
                    "error": ERROR_EMPTY_FILE}

        file_key = self.get_key(file_name)

        result = self.redis.set(file_key, file_contents)
        return result

    def delete(self, file_name):
        file_key = self.get_key(file_name)
        return self.redis.delete(file_key)
