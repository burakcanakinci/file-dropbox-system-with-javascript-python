import psycopg2
import uuid
from psycopg2 import Error, extras, errorcodes
from src.auth import db_driver
# import db_driver

ERROR_USER_NOT_FOUND = "User not found"
ERROR_USER_NAME_ALREADY_EXISTS = "User name already exists"


class UserDB:
    def __init__(self, db_config):
        self.db_driver = db_driver.DBDriver()
        self.db_driver.connect(db_config)
        self.db_driver.create_users_table()

    def create_user(self, user_details):
        psycopg2.extras.register_uuid()
        create_user_query = '''INSERT INTO users(id, name, role, access_token, logged_in, created_at, updated_at) VALUES ((%s), (%s), (%s), (%s), (%s), now(), now())'''

        cursor = self.db_driver.connection.cursor()
        try:
            cursor.execute(create_user_query, [user_details["id"],
                                               user_details["name"],
                                               user_details["role"],
                                               user_details["access_token"],
                                               user_details["logged_in"]])
            self.db_driver.connection.commit()
        except psycopg2.Error as err:
            self.db_driver.connection.rollback()

            if err.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                err = ERROR_USER_NAME_ALREADY_EXISTS

            return {"user_created": False,
                    "error": err}
        else:
            return {"user_created": True}
        finally:
            cursor.close()

    def get_user(self, user_id):
        psycopg2.extras.register_uuid()
        get_user_query = '''SELECT id, name, role, access_token, logged_in, created_at, updated_at FROM users WHERE id = (%s)'''

        cursor = self.db_driver.connection.cursor()
        try:
            cursor.execute(get_user_query, [user_id])
            self.db_driver.connection.commit()
        except psycopg2.Error as err:
            self.db_driver.connection.rollback()
            return {"user_fetched": False,
                    "error": err}
        else:
            user = cursor.fetchone()
            if user is not None:
                return {"user_fetched": True,
                        "id": user[0],
                        "name": user[1],
                        "role": user[2],
                        "access_token": user[3],
                        "logged_in": user[4]}
            else:
                return {"user_fetched": False,
                        "error": ERROR_USER_NOT_FOUND}
        finally:
            cursor.close()

    def login(self, user_name, access_token):
        psycopg2.extras.register_uuid()
        login_query = '''UPDATE users SET access_token = (%s), logged_in = (%s), updated_at = now() WHERE name = (%s) RETURNING id'''

        cursor = self.db_driver.connection.cursor()
        try:
            cursor.execute(login_query, [access_token, True, user_name])
            self.db_driver.connection.commit()
        except psycopg2.Error as err:
            self.db_driver.connection.rollback()
            return {"user_logged_in": False,
                    "error": err}
        else:
            if cursor.rowcount == 1:
                return {"user_logged_in": True,
                        "user_id": cursor.fetchone()[0]}
            else:
                return {"user_logged_in": False,
                        "error": ERROR_USER_NOT_FOUND}
        finally:
            cursor.close()

    def logout(self, user_name):
        logout_query = '''UPDATE users SET logged_in = (%s) WHERE name = (%s)'''

        cursor = self.db_driver.connection.cursor()
        try:
            cursor.execute(logout_query, [False, user_name])
            self.db_driver.connection.commit()
        except psycopg2.Error as err:
            self.db_driver.connection.rollback()
            return {"user_logged_out": False,
                    "error": err}
        else:
            if cursor.rowcount == 1:
                return {"user_logged_out": True}
            else:
                return {"user_logged_out": False,
                        "error": ERROR_USER_NOT_FOUND}
        finally:
            cursor.close()
