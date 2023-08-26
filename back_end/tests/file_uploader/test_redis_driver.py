import pytest
import sys
sys.path.append('../')

from src.file_uploader.redis_driver import RedisDriver, ERROR_KEY_NOT_FOUND  # NOQA

test_redis_config = {"service_name": "mymaster",
                     "master_host": "localhost",
                     "master_port": 26379,
                     "slave_1_host": "localhost",
                     "slave_1_port": 26379,
                     "slave_2_host": "localhost",
                     "slave_2_port": 26379,
                     "slave_3_host": "localhost",
                     "slave_3_port": 26379}


def teardown_redis(redis_conn):
    if redis_conn is not None:
        master = redis_conn.master_for("mymaster")
        master.flushall()


def test_connect():
    r = RedisDriver(test_redis_config)

    master = r.connection.master_for(r.service)
    master.set("hello", "world")

    master = r.connection.master_for(r.service)
    value = master.get("hello")
    assert value == "world"
    teardown_redis(r.connection)


def test_set():
    r = RedisDriver(test_redis_config)
    """
    success : set normal string value
    """
    result = r.set("test_key", "test_value")
    assert result["success"] == True

    master = r.connection.master_for(r.service)
    value = master.get("test_key")
    assert value == "test_value"

    """
    success : set non-string value
    """
    result = r.set("test_key2", {"k1": 1})
    assert result["success"] == True
    teardown_redis(r.connection)


def test_get():
    r = RedisDriver(test_redis_config)
    """
    failure : key doesn't exist
    """
    result = r.get("random_key")
    assert result["success"] == False
    assert result["error"] == ERROR_KEY_NOT_FOUND

    """
    success
    """
    master = r.connection.master_for(r.service)
    master.set("hello", "world")

    result = r.get("hello")
    assert result["success"] == True
    assert result["value"] == "world"
    teardown_redis(r.connection)


def test_delete():
    r = RedisDriver(test_redis_config)
    """
    success
    """
    master = r.connection.master_for(r.service)
    master.set("hello", "world")

    result = r.delete("hello")
    assert result["success"] == True

    master = r.connection.master_for(r.service)
    fetched_value = master.get("test_key")
    assert fetched_value == None
