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
    logging.info("[Authentication] Starting server")
    return


def log_create_user_req_received(name, role):
    logging.info(
        "[Authentication][CreateUserHandler] Received Request : user_name = " + name + " role = " + role)
    return


def log_create_user_success(name, role, id):
    logging.info(
        "[Authentication][CreateUserHandler] 201 Created Success : user_name = " + name + " role = " + role + "user_id = " + str(id))
    return


def log_create_user_bad_request(name, role, error_msg):
    logging.error("[Authentication][CreateUserHandler] 400 Bad Request : user_name = " +
                  name + " role = " + role + " :  error = " + error_msg)
    return


def log_create_user_internal_server_error(name, role, error_msg):
    logging.error("[Authentication][CreateUserHandler] 500 Internal Server Error : user_name = " +
                  name + " role = " + role + " :  error = " + error_msg)
    return


def log_login_req_received(name):
    logging.info(
        "[Authentication][LoginHandler] Received Request : user_name = " + name)
    return


def log_login_success(name, id):
    logging.info(
        "[Authentication][LoginHandler] 201 Created Success : user_name = " + name + " user_id = " + str(id))
    return


def log_login_bad_request(name, error_msg):
    logging.error(
        "[Authentication][LoginHandler] 400 Bad Request : user_name = " + name + " : error = " + error_msg)
    return


def log_login_internal_server_error(name, error_msg):
    logging.error(
        "[Authentication][LoginHandler] 500 Internal Server Error : user_name = " + name + " : error = " + error_msg)
    return


def log_logout_req_received(name):
    logging.info(
        "[Authentication][LogoutHandler] Received Request : user_name = " + name)
    return


def log_logout_success(name):
    logging.info(
        "[Authentication][LogoutHandler] 200 Success : user_name = " + name)
    return


def log_logout_bad_request(name, error_msg):
    logging.error(
        "[Authentication][LogoutHandler] 400 Bad Request : user_name = " + name + " : error = " + error_msg)
    return


def log_logout_internal_server_error(name, error_msg):
    logging.error(
        "[Authentication][LogoutHandler] 500 Internal Server Error : user_name = " + name + " : error = " + error_msg)
    return


def log_authenticate_req_received(id, token):
    logging.info(
        "[Authentication][AuthenticateUserHandler] Received Request : user_id = " + str(id) + " access_token = " + str(token))
    return


def log_authenticate_success(id, token):
    logging.info(
        "[Authentication][AuthenticateUserHandler] 200 Success : user_id = " + str(id) + " access_token = " + str(token))
    return


def log_authenticate_bad_request(id, token, error_msg):
    logging.error(
        "[Authentication][AuthenticateUserHandler] 400 Bad Request : user_id = " + str(id) + " access_token = " + str(token) + " : error = " + error_msg)
    return


def log_authenticate_unauthorised_request(id, token, error_msg):
    logging.error(
        "[Authentication][AuthenticateUserHandler] 401 Unauthorised Request : user_id = " + str(id) + " access_token = " + str(token) + " : error = " + error_msg)
    return


def log_authenticate_internal_server_error(id, token, error_msg):
    logging.error(
        "[Authentication][AuthenticateUserHandler] 500 Internal Server Error : user_id = " + str(id) + " access_token = " + " : error = " + error_msg)
    return


def log_db_connection_success():
    logging.info("[Authentication][PostgresDBDriver] Connected Successfully")
    return


def log_db_connection_error(error_msg):
    logging.info(
        "[Authentication][PostgresDBDriver] Faile to connect : " + error_msg)
    return
