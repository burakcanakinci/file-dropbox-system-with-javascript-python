import uuid
import time
import json
from src.file_uploader import index_cache
# import index_cache

MAX_FILE_UPLOAD_ATTEMPTS = 3


class FileUploader:
    def __init__(self, file_cache, file_queue_manager, user_queue_manager, admin_queue_manager, index_cache):
        self.file_cache = file_cache
        self.file_queue_manager = file_queue_manager
        self.user_queue_manager = user_queue_manager
        self.admin_queue_manager = admin_queue_manager
        self.index_cache = index_cache

    def send_file_for_upload(self, file_path, user_id, user_name, metadata):
        file_name = str(uuid.uuid4())

        result = self.file_cache.store(file_path, file_name)
        if not result["success"]:
            result["error_msg"] = "Error while storing the file contents in cache : " + result["error"]
            return result

        file_cache_key = self.file_cache.get_key(file_name)

        result = self.index_cache.create(file_name, metadata)
        if not result["success"]:
            result["error_msg"] = "Error while creating file index on the cache : " + result["error"]
            return result

        result = self.__publish_file_upload_queue_event(
            file_name, file_cache_key, user_id, user_name, metadata)
        if not result["message_published"]:
            result["success"] = False
            result["error_msg"] = "Error while publishing file upload event to queue : " + result["error"]
            return result

        result = self.__publish_client_notification_queue_event(
            file_name, user_id, user_name, index_cache.STATUS_FILE_CACHED)
        if not result["message_published"]:
            result["success"] = False
            return result

        return {"success": True,
                "file_name": file_name}

    def delete_uploaded_file(self, file_name, user_id, user_name):
        result = self.file_cache.delete(file_name)
        if not result["success"]:
            result["error_msg"] = "Error while deleting the file from cache : " + \
                result["error"]
            return result

        result = self.index_cache.update_uploaded(file_name)
        if not result["success"]:
            result["error_msg"] = "Error while updating file status in index cache : " + \
                result["error"]
            return result

        result = self.__publish_client_notification_queue_event(
            file_name, user_id, user_name, index_cache.STATUS_FILE_UPLOADED)
        if not result["message_published"]:
            result["success"] = False
            return result

        return {"success": True}

    def handle_failed_upload(self, file_name, user_id, user_name):
        result = self.index_cache.update_retry(
            file_name, MAX_FILE_UPLOAD_ATTEMPTS)

        if not result["success"]:
            if result["error"] == index_cache.ERROR_MAX_ATTEMPTS_REACHED:
                result = self.__handle_max_retried_upload(
                    file_name, user_id, user_name)
                if result["success"]:
                    return {"success":  False,
                            "error": index_cache.ERROR_MAX_ATTEMPTS_REACHED}

            error_msg = "Error while retrying file upload : " + \
                result["error"]
            return {"success": False,
                    "error": error_msg}

        file_cache_key = self.file_cache.get_key(file_name)
        metadata = result["metadata"]

        result = self.__publish_file_upload_queue_event(
            file_name, file_cache_key, user_id, user_name, metadata)

        if not result["message_published"]:
            result["success"] = False
            result["error"] = "Error while retrying file upload : Error while publishing to file upload queue : " + \
                result["error"]
            return result

        result["success"] = True
        return result

    def __handle_max_retried_upload(self, file_name, user_id, user_name):
        result = self.file_cache.delete(file_name)
        if not result["success"]:
            result["error"] = "Error while deleting file from cache : " + \
                result["error"]
            return result

        result = self.__publish_client_notification_queue_event(
            file_name, user_id, user_name, index_cache.STATUS_UPLOAD_FAILED)
        if not result["message_published"]:
            return {"success": False,
                    "error": result["error_msg"]}

        return {"success": True}

    def __publish_file_upload_queue_event(self, file_name, file_key, user_id, user_name, metadata):
        msg = {"id": str(uuid.uuid4()),
               "file_name": file_name,
               "file_cache_key": file_key,
               "file_metadata": metadata,
               "user_id": user_id,
               "user_name": user_name,
               "event_timestamp": time.time()}

        msg_json = json.dumps(msg)
        return self.file_queue_manager.publish(msg_json)

    def __publish_client_notification_queue_event(self, file_name, user_id, user_name, status):
        msg = {"id": str(uuid.uuid4()),
               "file_name": file_name,
               "status": status,
               "user_id": user_id,
               "user_name": user_name,
               "event_timestamp": time.time()}

        msg_json = json.dumps(msg)
        result = self.user_queue_manager.publish(msg_json)
        if not result["message_published"]:
            result["error_msg"] = "Error while publishing message to user notification queue : " + result["error"]
            return result

        result = self.admin_queue_manager.publish(msg_json)
        if not result["message_published"]:
            result["error_msg"] = "Error while publishing message to admin notification queue : " + result["error"]
            return result

        return result
