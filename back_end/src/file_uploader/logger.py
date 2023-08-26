import logging
import logging.handlers


def setup(log_file_path):
    logger = logging.getLogger()
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file_path, maxBytes=10240, backupCount=5)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
    return


def log_server_start():
    logging.info("[File Uploader] Starting server")
    return


def log_ping():
    logging.debug("[File Uploader][Ping] Received Ping")
    return


def log_upload_req_received(user_id, user_name):
    logging.info("[File Uploader][FileUploadHandler] Received Request : user_id = " +
                 user_id + " and user_name = " + user_name)
    return


def log_upload_success(user_id, user_name):
    logging.info("[File Uploader][FileUploadHandler] 201 Created Success : user_id = " +
                 user_id + " and user_name = " + user_name)


def log_upload_bad_request(user_id, user_name, error_msg):
    logging.error("[File Uploader][FileUploadHandler] 400 Bad Request : user_id = " +
                  user_id + " and user_name = " + user_name + " : error = " + error_msg)
    return


def log_upload_internal_server_error(user_id, user_name, error_msg):
    logging.error("[File Uploader][FileUploadHandler] 500 Internal Server Error : from user_id = " +
                  user_id + " and user_name = " + user_name + " : error =" + error_msg)
    return


def log_status_update_req_received(user_id, user_name, file_id, status):
    logging.info("[File Uploader][UpdateFileStatusHandler] Request Receieved : for user_id = " +
                 user_id + " and user_name = " + user_name + " : file_id = " + file_id + " file_status = " + status)
    return


def log_status_update_success(user_id, user_name, file_id, status):
    logging.info("[File Uploader][UpdateFileStatusHandler] 200 Success : for user_id = " +
                 user_id + " and user_name = " + user_name + " : file_id = " + file_id + " file_status = " + status)
    return


def log_status_update_bad_request(user_id, user_name, file_id, status, error_msg):
    logging.error("[File Uploader][UpdateFileStatusHandler] 400 Bad Request : for user_id = " +
                  user_id + " and user_name = " + user_name + " : file_id = " + file_id + " file_status = " + status + " : error = " + error_msg)
    return


def log_status_update_internal_server_error(user_id, user_name, file_id, status, error_msg):
    logging.error("[File Uploader][UpdateFileStatusHandler] 500 Internal Server Error : for user_id = " +
                  user_id + " and user_name = " + user_name + " : file_id = " + file_id + " file_status = " + status + " : error = " + error_msg)
    return


def log_status_update_max_retries(user_id, user_name, file_id, status):
    logging.warn("[File Uploader][UpdateFileStatusHandler] File upload retried maximum number of times : for user_id = " +
                 user_id + " and user_name = " + user_name + " : file_id = " + file_id + " file_status = " + status)
    return


def log_redis_connection_success():
    logging.info("[FileUploader][RedisDriver] : Connected to Redis")
    return


def log_redis_connection_error(error_str):
    logging.error("[FileUploader][RedisDriver] : " + error_str)
    return


def log_rabbitmq_connection_success():
    logging.info("[FileUploader][RabbitMQManager] : Connected to RabbitMQ")
    return


def log_rabbitmq_connection_error(error_str):
    logging.error("[FileUploader][RabbitMQManager] : " + error_str)
    return
