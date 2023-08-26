import os
import jwt
from flask import Flask
from flask_restful import Resource, Api, output_json, reqparse
from uuid import UUID
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.auth import authentication_service
from src.auth import user_db
from src.auth import logger
# import authentication_service
# import user_db
# import logger


INSIDE_CONTAINER = os.environ.get('IN_CONTAINER_FLAG', False)

app = Flask(__name__)
CORS(app, supports_credentials=True)

api = Api(app)
CORS(app, supports_credentials=True)


ERROR_ROLE_NOT_PROVIDED = "Role not provided"
ERROR_NAME_NOT_PROVIDED = "Name not provided"
ERROR_ROLE_NOT_FOUND = "Invalid role"
ERROR_USER_ID_NOT_PROVIDED = "User id not provided"
ERROR_ACCESS_TOKEN_NOT_PROVIDED = "Access token not provided"
ERROR_INVALID_USER_ID = "Inavlid User ID"
ERROR_INVALID_USER_NAME = "Inavlid User Name"
ERROR_INVALID_ACCESS_TOKEN = "Inavlid Access Token"
ERROR_INTERNAL_SERVER = "Internal Server Error"
ERROR_UNAUTHORISED_USER = "User is unauthorised with this access token"
STATUS_USER_AUTHORISED = "User authorised with this access token"

SECRET_KEY = "i5uitypjchnar0rlz31yh0u5sgs8rui2baxxgw8e"
LOG_FILE_PATH = "logs/log_file.txt"

app.config['SECRET_KEY'] = SECRET_KEY
jwtMng = JWTManager(app)

if INSIDE_CONTAINER:
    db_config = {"user": "postgres",
                 "password": "postgres",
                 "host": "postgresdb",
                 "port": "5432",
                 "db_name": "user_auth"}
else:
    db_config = {"user": "postgres",
                 "password": "postgres",
                 "host": "127.0.0.1",
                 "port": "5432",
                 "db_name": "user_auth"}

accepted_roles = ["admin", "user", "developer"]


def init(db_config):
    db = user_db.UserDB(db_config)
    svc = authentication_service.Authenticator(db)
    return svc


def is_valid_uuid(uuid_str):
    try:
        uuid_obj = UUID(uuid_str, version=4)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_str


def is_valid_user_name(user_name):
    cleaned_user_name = user_name.strip()
    return not (cleaned_user_name == "")


def create_jwt(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


class Ping(Resource):
    def get(self):
        return output_json({"ping": "pong"}, 200)


class CreateUser(Resource):
    def __init__(self, svc):
        self.svc = svc

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str,
                            help=ERROR_NAME_NOT_PROVIDED)
        parser.add_argument('role', required=True, type=str,
                            help=ERROR_ROLE_NOT_PROVIDED)
        args = parser.parse_args()

        role, name = args["role"], args["name"]

        logger.log_create_user_req_received(name, role)

        if role not in accepted_roles:
            logger.log_create_user_bad_request(
                name, role, ERROR_ROLE_NOT_FOUND)
            return output_json({"msg": ERROR_ROLE_NOT_FOUND}, 400)

        user_details = svc.create_user(role, name)
        if user_details["user_created"]:
            user_details["id"] = str(user_details["id"])
            user_details["access_token"] = str(user_details["access_token"])
            jwt = create_jwt(user_details)

            logger.log_create_user_success(name, role, user_details["id"])
            return output_json({"jwt": jwt.decode()}, 201)

        elif user_details["error"] == user_db.ERROR_USER_NAME_ALREADY_EXISTS:
            logger.log_create_user_bad_request(
                name, role, user_db.ERROR_USER_NAME_ALREADY_EXISTS)
            return output_json({"msg": user_db.ERROR_USER_NAME_ALREADY_EXISTS}, 400)

        else:
            logger.log_create_user_internal_server_error(
                name, role, result["error"])
            return output_json({"msg": ERROR_INTERNAL_SERVER}, 500)


class LoginUser(Resource):
    def __init__(self, svc):
        self.svc = svc

    def put(self, user_name):
        logger.log_login_req_received(user_name)

        if not is_valid_user_name(user_name):
            logger.log_login_bad_request(user_name, ERROR_INVALID_USER_NAME)
            return output_json({"msg": ERROR_INVALID_USER_NAME}, 400)

        response = svc.login(user_name)
        if response["user_logged_in"]:
            response["access_token"] = str(response["access_token"])
            response["user_id"] = str(response["user_id"])
            jwt = create_jwt(response)

            logger.log_login_success(user_name, response["user_id"])
            return output_json({"jwt": jwt.decode()}, 201)

        elif response["error"] == user_db.ERROR_USER_NOT_FOUND:
            logger.log_login_bad_request(
                user_name, user_db.ERROR_USER_NOT_FOUND)
            return output_json(response, 400)

        else:
            logger.log_login_internal_server_error(
                user_name, response["error"])
            return output_json({"msg": ERROR_INTERNAL_SERVER}, 500)


class LogoutUser(Resource):
    def __init__(self, svc):
        self.svc = svc

    def put(self, user_name):
        logger.log_logout_req_received(user_name)

        if not is_valid_user_name(user_name):
            logger.log_logout_bad_request(user_name, ERROR_INVALID_USER_NAME)
            return output_json({"msg": ERROR_INVALID_USER_NAME}, 400)

        response = svc.logout(user_name)
        if response["user_logged_out"]:
            logger.log_logout_success(user_name)
            return output_json(response, 200)

        elif response["error"] == user_db.ERROR_USER_NOT_FOUND:
            logger.log_logout_bad_request(
                user_name, user_db.ERROR_USER_NOT_FOUND)
            return output_json(response, 400)

        else:
            logger.log_logout_internal_server_error(
                user_name, response["error"])
            return output_json({"msg": ERROR_INTERNAL_SERVER}, 500)


class AuthenticateUser(Resource):
    def __init__(self, svc):
        self.svc = svc

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=str,
                            help=ERROR_USER_ID_NOT_PROVIDED)
        parser.add_argument('access_token', required=True, type=str,
                            help=ERROR_ACCESS_TOKEN_NOT_PROVIDED)

        args = parser.parse_args()
        user_id, access_token = args["user_id"], args["access_token"]

        logger.log_authenticate_req_received(user_id, access_token)

        if not is_valid_uuid(user_id):
            logger.log_authenticate_bad_request(
                user_id, access_token, ERROR_INVALID_USER_ID)
            return output_json({"msg": ERROR_INVALID_USER_ID}, 400)

        if not is_valid_uuid(access_token):
            logger.log_authenticate_bad_request(
                user_id, access_token, ERROR_INVALID_ACCESS_TOKEN)
            return output_json({"msg": ERROR_INVALID_ACCESS_TOKEN}, 400)

        fetched_user = svc.get_user(user_id, access_token)
        if not fetched_user["user_fetched"]:

            if fetched_user["error"] == authentication_service.ERROR_UNAUTHORISED_REQUEST:
                logger.log_authenticate_unauthorised_request(
                    user_id, access_token, ERROR_UNAUTHORISED_USER)
                return output_json({"msg": ERROR_UNAUTHORISED_USER}, 401)

            if fetched_user["error"] == user_db.ERROR_USER_NOT_FOUND:
                logger.log_authenticate_bad_request(
                    user_id, access_token, user_db.ERROR_USER_NOT_FOUND)
                return output_json({"msg": user_db.ERROR_USER_NOT_FOUND}, 400)

            logger.log_authenticate_internal_server_error(
                user_id, access_token, fetched_user["error"])
            return output_json({"msg": ERROR_INTERNAL_SERVER}, 500)

        logger.log_authenticate_success(user_id, access_token)
        return output_json({"msg": STATUS_USER_AUTHORISED}, 200)


svc = init(db_config)

api.add_resource(Ping, '/ping')
api.add_resource(CreateUser, '/auth/signup',
                 resource_class_kwargs={"svc": svc})
api.add_resource(LoginUser, '/auth/login/<string:user_name>',
                 resource_class_kwargs={"svc": svc})
api.add_resource(LogoutUser, '/auth/logout/<string:user_name>',
                 resource_class_kwargs={"svc": svc})
api.add_resource(AuthenticateUser, '/auth/validate',
                 resource_class_kwargs={"svc": svc})

if __name__ == '__main__':
    logger.setup(LOG_FILE_PATH)

    logger.log_server_start()
    app.run(debug=True, use_debugger=False, use_reloader=False,
            passthrough_errors=True, host='0.0.0.0', port=4000)
