import pytest
from pytest_mock import mocker
import sys
import os
sys.path.append('../')

from src.file_uploader.file_cache import FileCache, ERROR_FILE_NOT_FOUND, ERROR_EMPTY_FILE  # NOQA
from src.file_uploader.redis_driver import RedisDriver, ERROR_KEY_NOT_FOUND  # NOQA

test_redis_config = {"service_name": "mymaster",
                     "master_host": "127.0.0.1",
                     "master_port": 26379,
                     "slave_1_host": "127.0.0.1",
                     "slave_1_port": 26379,
                     "slave_2_host": "127.0.0.1",
                     "slave_2_port": 26379,
                     "slave_3_host": "127.0.0.1",
                     "slave_3_port": 26379}


def teardown_redis(redis_conn):
    if redis_conn is not None:
        master = redis_conn.get_master("mymaster")
        master.flushall()


def test_store(mocker):
    cache = FileCache(test_redis_config)
    """
    failure : file does not exist
    """
    file_name = "random_file.txt"
    file_path = "some/path/"+file_name

    result = cache.store(file_path, file_name)
    assert result["success"] == False
    assert result["error"] == ERROR_FILE_NOT_FOUND

    key = "file:random_file.txt"
    fetched_file = cache.redis.get(key)
    assert fetched_file["success"] == False
    assert fetched_file["error"] == ERROR_KEY_NOT_FOUND

    """
    failure : file is empty
    """
    file_name = "test_file.txt"
    file_path = "./"+file_name
    file = open(file_path, "w")
    file.close()

    result = cache.store(file_path, file_name)
    assert result["success"] == False
    assert result["error"] == ERROR_EMPTY_FILE

    key = "file:test_file.txt"
    fetched_file = cache.redis.get(key)
    assert fetched_file["success"] == False
    assert fetched_file["error"] == ERROR_KEY_NOT_FOUND

    """
    success
    """
    file_name = "test_file.txt"
    file_path = "./"+file_name

    file = open(file_path, "w+")
    file_content = "Hello World"
    file.write(file_content)
    file.close()

    result = cache.store(file_path, file_name)
    assert result["success"] == True

    key = "file:test_file.txt"
    fetched_file = cache.redis.get(key)
    assert fetched_file["success"] == True
    assert fetched_file["value"] == str(file_content.encode('utf-8'))

    teardown_redis(cache.redis.connection)

    """
    failure : redis not available
    """
    def mock_redis_set(obj, key, value):
        return {"success": False,
                "error": "some error from redis"}

    mocker.patch.object(RedisDriver, 'set', new=mock_redis_set)
    cache = FileCache(test_redis_config)

    result = cache.store(file_path, file_name)
    assert result["success"] == False
    assert result["error"] == "some error from redis"

    os.remove(file_name)


def test_delete(mocker):
    cache = FileCache(test_redis_config)
    file_name = "test_file.txt"
    """
    success : file does not exist
    """

    result = cache.delete(file_name)
    assert result["success"] == True

    """
    success : files exists
    """
    key = "file:" + file_name
    file_content = "Hello World".encode('utf-8')
    master = cache.redis.connection.master_for(cache.redis.service)
    master.set(key, file_content)

    result = cache.delete(file_name)
    assert result["success"] == True

    value = master.get(key)
    assert value == None

    teardown_redis(cache.redis.connection)

    """
    failure : redis not available
    """
    def mock_redis_delete(obj, key):
        return {"success": False,
                "error": "some error from redis"}

    mocker.patch.object(RedisDriver, 'delete', new=mock_redis_delete)
    cache = FileCache(test_redis_config)

    result = cache.delete(file_name)
    assert result["success"] == False
    assert result["error"] == "some error from redis"
