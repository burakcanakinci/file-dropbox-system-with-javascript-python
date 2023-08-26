import pytest
from pytest_mock import mocker
import sys
import json
sys.path.append('../')

from src.file_uploader import index_cache  # NOQA
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
        master = redis_conn.master_for("mymaster")
        master.flushall()


def test_create(mocker):
    file_name = "file1"
    metadata = {"key1": "value1", "key2": "value2"}
    metadata_str = json.dumps(metadata)

    """
    success
    """
    cache = index_cache.IndexCache(test_redis_config)
    result = cache.create(file_name, metadata_str)
    assert result["success"] == True

    key = "file_index:" + file_name
    result = cache.redis.get(key)
    assert result["success"] == True

    value = json.loads(result["value"])
    assert value["status"] == index_cache.STATUS_FILE_CACHED
    assert value["metadata"] == metadata_str
    assert value["attempt"] == 1

    teardown_redis(cache.redis.connection)

    """
    failure : redis fails
    """
    def mock_redis_set(obj, key, val):
        return {"success": False,
                "error": "some redis error"}

    mocker.patch.object(RedisDriver, 'set', new=mock_redis_set)

    cache = index_cache.IndexCache(test_redis_config)
    result = cache.create(file_name, metadata_str)
    assert result["success"] == False
    assert result["error"] == "some redis error"


def test_update_uploaded(mocker):
    file_name = "file1"
    index_key = "file_index:" + file_name

    metadata = {"key1": "value1", "key2": "value2"}
    metadata_str = json.dumps(metadata)

    value = {"status": "old_status", "metadata": metadata_str, "attempt": 2}
    val_json = json.dumps(value)

    cache = index_cache.IndexCache(test_redis_config)

    """
    success
    """

    result = cache.redis.set(index_key, val_json)
    assert result["success"] == True

    result = cache.update_uploaded(file_name)
    assert result["success"] == True

    result = cache.redis.get(index_key)
    assert result["success"] == True

    value = json.loads(result["value"])
    assert value["status"] == index_cache.STATUS_FILE_UPLOADED
    assert value["metadata"] == metadata_str
    assert value["attempt"] == 2

    teardown_redis(cache.redis.connection)

    """
    failure : key doesn't exist
    """
    result = cache.update_uploaded(file_name)
    assert result["success"] == False
    assert result["error"] == ERROR_KEY_NOT_FOUND

    """
    failure : redis is not responsive while getting the key
    """
    def mock_redis_get(obj, key):
        return {"success": False,
                "error": "Redis not responding"}

    mocker.patch.object(RedisDriver, 'get', new=mock_redis_get)

    cache = index_cache.IndexCache(test_redis_config)
    result = cache.update_uploaded(file_name)
    assert result["success"] == False
    assert result["error"] == "Redis not responding"

    """
    failure : redis is not responsive while setting the key
    """
    def mock_redis_get(obj, key):
        return {"success": True,
                "value": val_json}

    def mock_redis_set(obj, key, value):
        return {"success": False,
                "error": "Redis not responding"}

    mocker.patch.object(RedisDriver, 'get', new=mock_redis_get)
    mocker.patch.object(RedisDriver, 'set', new=mock_redis_set)

    cache = index_cache.IndexCache(test_redis_config)
    result = cache.update_uploaded(file_name)
    assert result["success"] == False
    assert result["error"] == "Redis not responding"


def test_update_retry(mocker):
    file_name = "file2"
    index_key = "file_index:" + file_name

    metadata = {"key1": "value1", "key2": "value2"}
    metadata_str = json.dumps(metadata)

    max_attempts = 3

    value = {"status": "old_status", "metadata": metadata_str, "attempt": 2}
    val_json = json.dumps(value)

    cache = index_cache.IndexCache(test_redis_config)

    """
    success
    """
    result = cache.redis.set(index_key, val_json)
    assert result["success"] == True

    result = cache.update_retry(file_name, max_attempts)
    assert result["success"] == True
    assert result["metadata"] == metadata_str

    result = cache.redis.get(index_key)
    assert result["success"] == True

    value = json.loads(result["value"])
    assert value["status"] == index_cache.STATUS_RETRY_UPLOAD
    assert value["metadata"] == metadata_str
    assert value["attempt"] == 3

    """
    failure : max attempts reached
    """
    result = cache.update_retry(file_name, max_attempts)
    assert result["success"] == False
    assert result["error"] == index_cache.ERROR_MAX_ATTEMPTS_REACHED

    result = cache.redis.get(index_key)
    assert result["success"] == True

    value = json.loads(result["value"])
    assert value["status"] == index_cache.STATUS_UPLOAD_FAILED
    assert value["attempt"] == 3

    teardown_redis(cache.redis.connection)

    """
    failure : key not found
    """
    result = cache.update_retry(file_name, max_attempts)
    assert result["success"] == False
    assert result["error"] == ERROR_KEY_NOT_FOUND

    """
    failure : redis not responsive while checking if key exists
    """
    def mock_redis_get(obj, key):
        return {"success": False,
                "error": "Redis not responding"}

    mocker.patch.object(RedisDriver, 'get', new=mock_redis_get)

    cache = index_cache.IndexCache(test_redis_config)
    result = cache.update_retry(file_name, max_attempts)
    assert result["success"] == False
    assert result["error"] == "Redis not responding"

    """
    failure : redis is not responsive while setting the key
    """
    def mock_redis_get(obj, key):
        return {"success": True,
                "value": val_json}

    def mock_redis_set(obj, key, value):
        return {"success": False,
                "error": "Redis not responding"}

    mocker.patch.object(RedisDriver, 'get', new=mock_redis_get)
    mocker.patch.object(RedisDriver, 'set', new=mock_redis_set)

    cache = index_cache.IndexCache(test_redis_config)
    result = cache.update_retry(file_name, max_attempts)
    assert result["success"] == False
    assert result["error"] == "Redis not responding"
