import pytest
import uuid
import sys
import psycopg2
from psycopg2 import Error, errorcodes
sys.path.append('../')

from src.auth.user_db import UserDB, ERROR_USER_NOT_FOUND, ERROR_USER_NAME_ALREADY_EXISTS  # NOQA


def test_db():
    test_db_config = {"user": "postgres",
                      "password": "postgres",
                      "host": "127.0.0.1",
                      "port": "5432",
                      "db_name": "user_auth_test"}

    db = UserDB(test_db_config)
    return db


def tear_down(cursor, db_driver):
    cursor.execute("TRUNCATE users;")
    db_driver.connection.commit()
    cursor.close()
    # db_driver.connection.close()


def test_create_user():
    """
    success
    """
    db = test_db()
    user_details = {"id": uuid.uuid4(),
                    "name": "user-1",
                    "role": "dummy",
                    "access_token": uuid.uuid4(),
                    "logged_in": True}
    result = db.create_user(user_details)
    assert result["user_created"] == True

    cursor = db.db_driver.connection.cursor()
    fetched_user = get_test_user(db, cursor, user_details["id"])
    assert fetched_user["user_fetched"] == True
    assert fetched_user["id"] == user_details["id"]
    assert fetched_user["name"] == user_details["name"]
    assert fetched_user["role"] == user_details["role"]
    assert fetched_user["access_token"] == user_details["access_token"]
    assert fetched_user["logged_in"] == user_details["logged_in"]

    """
    failure : when user_id is not uuid
    """
    user_details = {"id": "some_random_id",
                    "name": "user-1",
                    "role": "dummy",
                    "access_token": uuid.uuid4(),
                    "logged_in": True}
    result = db.create_user(user_details)
    assert result["user_created"] == False
    assert result["error"].pgcode == '22P02'
    assert result["error"].pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION

    """
    failure : when user_name violates uniqueness constraint
    """
    user_details = {"id": uuid.uuid4(),
                    "name": "user-2",
                    "role": "dummy",
                    "access_token": uuid.uuid4(),
                    "logged_in": True}
    create_test_user(
        db, cursor, user_details["id"], user_details["name"], user_details["access_token"])

    user_details["id"] = uuid.uuid4()
    result = db.create_user(user_details)
    assert result["user_created"] == False
    assert result["error"] == ERROR_USER_NAME_ALREADY_EXISTS

    tear_down(cursor, db.db_driver)


def test_get_user():
    db = test_db()
    """
    failure : user does not exist
    """
    new_user_id = uuid.uuid4()
    fetched_user = db.get_user(new_user_id)
    print(new_user_id)
    print(fetched_user)
    assert fetched_user["user_fetched"] == False
    assert fetched_user["error"] == ERROR_USER_NOT_FOUND

    """
    success
    """
    user_id = uuid.uuid4()
    access_token = uuid.uuid4()

    create_user_query = '''INSERT INTO users(id, role, access_token, logged_in, created_at, updated_at) VALUES ((%s), (%s), (%s), (%s), now(), now())'''
    cursor = db.db_driver.connection.cursor()
    psycopg2.extras.register_uuid()

    try:
        cursor.execute(create_user_query, [
            user_id, "dummy", access_token, False])
        db.db_driver.connection.commit()
    except psycopg2.Error as err:
        print("Error in creating test user : ", err)

    fetched_user = db.get_user(user_id)
    assert fetched_user["user_fetched"] == True

    tear_down(cursor, db.db_driver)


def test_login():
    db = test_db()
    """
    failure : user doesn't exist
    """
    user_name = "user-1"
    access_token = uuid.uuid4()

    result = db.login(user_name, access_token)
    assert result["user_logged_in"] == False
    assert result["error"] == ERROR_USER_NOT_FOUND

    """
    success
    """
    user_id = uuid.uuid4()
    user_name = "user-1"
    access_token = uuid.uuid4()

    cursor = db.db_driver.connection.cursor()
    create_test_user(db, cursor, user_id, user_name, access_token)

    result = db.login(user_name, access_token)
    assert result["user_logged_in"] == True
    assert result["user_id"] == user_id

    fetched_user = get_test_user(db, cursor, user_id)

    assert fetched_user["user_fetched"] == True
    assert fetched_user["id"] == user_id
    assert fetched_user["access_token"] == access_token
    assert fetched_user["logged_in"] == True

    tear_down(cursor, db.db_driver)


def test_logout():
    db = test_db()
    """
    failure : user doesn't exist
    """
    user_name = "user-5"

    result = db.logout(user_name)
    assert result["user_logged_out"] == False
    assert result["error"] == ERROR_USER_NOT_FOUND

    """
    success
    """
    user_id = uuid.uuid4()
    access_token = uuid.uuid4()
    user_name = "user-2"

    cursor = db.db_driver.connection.cursor()
    create_test_user(db, cursor, user_id, user_name, access_token)

    result = db.logout(user_name)
    assert result["user_logged_out"] == True

    fetched_user = get_test_user(db, cursor, user_id)
    assert fetched_user["user_fetched"] == True
    assert fetched_user["name"] == user_name
    assert fetched_user["logged_in"] == False

    tear_down(cursor, db.db_driver)


def create_test_user(db, cursor, user_id, user_name, access_token):
    create_user_query = '''INSERT INTO users(id, name, role, access_token, logged_in, created_at, updated_at) VALUES ((%s), (%s), (%s), (%s), (%s), now(), now())'''
    psycopg2.extras.register_uuid()

    try:
        cursor.execute(create_user_query, [
            user_id, user_name, "admin", access_token, False])
        db.db_driver.connection.commit()
    except psycopg2.Error as err:
        print("Error in creating test user : ", err)


def get_test_user(db, cursor, user_id):
    get_user_query = '''SELECT id, name, role, access_token, logged_in, created_at, updated_at FROM users WHERE id = (%s)'''
    try:
        cursor.execute(get_user_query, [user_id])
        db.db_driver.connection.commit()
    except psycopg2.Error as err:
        print("Error while fetching the test user : ", err)
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
