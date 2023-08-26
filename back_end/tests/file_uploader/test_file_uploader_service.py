import pytest
from pytest_mock import mocker
import sys
import json
sys.path.append('../')

from src.file_uploader import file_uploader_service  # NOQA
from src.file_uploader.file_cache import FileCache  # NOQA
from src.file_uploader.index_cache import IndexCache, ERROR_MAX_ATTEMPTS_REACHED  # NOQA
from src.file_uploader.redis_driver import RedisDriver  # NOQA
from src.file_uploader.rabbitmq import RabbitMQManager  # NOQA

test_redis_config = {"service_name": "mymaster",
                     "master_host": "127.0.0.1",
                     "master_port": 26379,
                     "slave_1_host": "127.0.0.1",
                     "slave_1_port": 26379,
                     "slave_2_host": "127.0.0.1",
                     "slave_2_port": 26379,
                     "slave_3_host": "127.0.0.1",
                     "slave_3_port": 26379}

test_file_rabbitmq_config = {"user": "guest",
                             "password": "guest",
                             "host": "127.0.0.1",
                             "port": "5672",
                             "connection_timeout_s": 1200,
                             "idle_connection_timeout_s": 1800,
                             "connection_retry_s": 3,
                             "connection_retry_attempts": 5,
                             "queue_name": "test_file_uploads"}

test_user_rabbitmq_config = {"user": "guest",
                             "password": "guest",
                             "host": "127.0.0.1",
                             "port": "5672",
                             "connection_timeout_s": 1200,
                             "idle_connection_timeout_s": 1800,
                             "connection_retry_s": 3,
                             "connection_retry_attempts": 5,
                             "queue_name": "test_user_notification"}

test_admin_rabbitmq_config = {"user": "guest",
                              "password": "guest",
                              "host": "127.0.0.1",
                              "port": "5672",
                              "connection_timeout_s": 1200,
                              "idle_connection_timeout_s": 1800,
                              "connection_retry_s": 3,
                              "connection_retry_attempts": 5,
                              "queue_name": "test_admin_notification"}


def test_send_file_for_upload(mocker):
    user_id = "user:1"
    user_name = "test_user"

    metadata = {"key1": "value1", "key2": "value2"}
    metadata_str = json.dumps(metadata)

    """
    failure : error while storing file in cache
    """
    def mock_file_cache_store(obj, file_path, file_name):
        return {"success": False,
                "error": "some_error"}

    mocker.patch.object(FileCache, 'store', new=mock_file_cache_store)

    file_cache = FileCache(test_redis_config)
    svc = file_uploader_service.FileUploader(
        file_cache, None, None, None, None)

    result = svc.send_file_for_upload(
        "/random/file/path", user_id, user_name, metadata_str)
    assert result["success"] == False
    assert result["error_msg"] == "Error while storing the file contents in cache : some_error"

    """
    failure : error while creating file index cache entry
    """
    def mock_file_cache_store(obj, file_path, file_name):
        return {"success": True}

    def mock_index_cache_create(obj, file_name, meta_data):
        return {"success": False,
                "error": "some_error_in_indexing"}

    mocker.patch.object(FileCache, 'store', new=mock_file_cache_store)
    mocker.patch.object(IndexCache, 'create', new=mock_index_cache_create)

    file_cache = FileCache(test_redis_config)
    index_cache = IndexCache(test_redis_config)
    svc = file_uploader_service.FileUploader(
        file_cache, None, None, None, index_cache)

    result = svc.send_file_for_upload(
        "/random/file/path", user_id, user_name, metadata_str)
    assert result["success"] == False
    assert result["error_msg"] == "Error while creating file index on the cache : some_error_in_indexing"

    """
    failure : error while publishing file upload event to rabbitmq
    """
    def mock_file_cache_store(obj, file_path, file_name):
        return {"success": True}

    def mock_index_cache_create(obj, file_name, meta_data):
        return {"success": True}

    def mock_publish(obj, msg_body):
        return {"message_published": False,
                "error": "something failing"}

    mocker.patch.object(FileCache, 'store', new=mock_file_cache_store)
    mocker.patch.object(IndexCache, 'create', new=mock_index_cache_create)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    file_cache = FileCache(test_redis_config)
    index_cache = IndexCache(test_redis_config)
    file_queue_manager = RabbitMQManager(test_file_rabbitmq_config)
    svc = file_uploader_service.FileUploader(
        file_cache, file_queue_manager, None, None, index_cache)

    result = svc.send_file_for_upload(
        "/random/file/path", user_id, user_name, metadata_str)
    assert result["success"] == False
    assert result["error_msg"] == "Error while publishing file upload event to queue : something failing"

    """
    success
    """
    def mock_file_cache_store(obj, file_path, file_name):
        return {"success": True}

    def mock_index_cache_create(obj, file_name, meta_data):
        return {"success": True}

    def mock_publish(obj, msg_body):
        return {"message_published": True}

    mocker.patch.object(FileCache, 'store', new=mock_file_cache_store)
    mocker.patch.object(IndexCache, 'create', new=mock_index_cache_create)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    file_cache = FileCache(test_redis_config)
    index_cache = IndexCache(test_redis_config)
    file_queue_manager = RabbitMQManager(test_file_rabbitmq_config)
    user_queue_manager = RabbitMQManager(test_user_rabbitmq_config)
    admin_queue_manager = RabbitMQManager(test_admin_rabbitmq_config)
    svc = file_uploader_service.FileUploader(
        file_cache, file_queue_manager, user_queue_manager, admin_queue_manager, index_cache)

    result = svc.send_file_for_upload(
        "/random/file/path", user_id, user_name, metadata_str)
    assert result["success"] == True


def test_delete_uploaded_file(mocker):
    user_id = "user-1"
    user_name = "hello123"
    """
    failure : error in deleting file from cache
    """
    def mock_file_cache_delete(obj, file_name):
        return {"success": False,
                "error": "some_error"}

    mocker.patch.object(FileCache, 'delete', new=mock_file_cache_delete)

    file_cache = FileCache(test_redis_config)
    svc = file_uploader_service.FileUploader(
        file_cache, None, None, None, None)

    result = svc.delete_uploaded_file("file1", user_id, user_name)
    assert result["success"] == False
    assert result["error_msg"] == "Error while deleting the file from cache : some_error"

    """
    failure : key not found in index cache
    """
    def mock_file_cache_delete(obj, file_name):
        return {"success": True,
                "file_key": "file:file_name"}

    def mock_redis_get(obj, key):
        return {"success": False,
                "error": "key not found"}

    mocker.patch.object(FileCache, 'delete', new=mock_file_cache_delete)
    mocker.patch.object(RedisDriver, 'get', new=mock_redis_get)

    file_cache = FileCache(test_redis_config)
    index_cache = IndexCache(test_redis_config)
    svc = file_uploader_service.FileUploader(
        file_cache, None, None, None, index_cache)

    result = svc.delete_uploaded_file("file1", user_id, user_name)
    assert result["success"] == False
    assert result["error_msg"] == "Error while updating file status in index cache : key not found"

    """
    failure : error in updating file index cache
    """
    def mock_file_cache_delete(obj, file_name):
        return {"success": True,
                "file_key": "file:file_name"}

    def mock_index_cache_update_uploaded(obj, file_name):
        return {"success": False,
                "error": "some_error_in_redis"}

    mocker.patch.object(FileCache, 'delete', new=mock_file_cache_delete)
    mocker.patch.object(IndexCache, 'update_uploaded',
                        new=mock_index_cache_update_uploaded)

    file_cache = FileCache(test_redis_config)
    index_cache = IndexCache(test_redis_config)
    svc = file_uploader_service.FileUploader(
        file_cache, None, None, None, index_cache)

    result = svc.delete_uploaded_file("file1", user_id, user_name)
    assert result["success"] == False
    assert result["error_msg"] == "Error while updating file status in index cache : some_error_in_redis"

    """
    failure : error in publishing user notification message
    """
    def mock_file_cache_delete(obj, file_name):
        return {"success": True,
                "file_key": "file:file_name"}

    def mock_index_cache_update_uploaded(obj, file_name):
        return {"success": True}

    def mock_publish(obj, msg_body):
        return {"message_published": False,
                "error": "some error from rabbitmq"}

    mocker.patch.object(FileCache, 'delete', new=mock_file_cache_delete)
    mocker.patch.object(IndexCache, 'update_uploaded',
                        new=mock_index_cache_update_uploaded)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    file_cache = FileCache(test_redis_config)
    index_cache = IndexCache(test_redis_config)
    user_queue_manager = RabbitMQManager(test_user_rabbitmq_config)
    admin_queue_manager = RabbitMQManager(test_admin_rabbitmq_config)

    svc = file_uploader_service.FileUploader(file_cache, None, user_queue_manager,
                                             admin_queue_manager, index_cache)

    result = svc.delete_uploaded_file("file1", user_id, user_name)
    assert result["success"] == False
    assert result["error_msg"] == "Error while publishing message to user notification queue : some error from rabbitmq"

    """
    success
    """
    def mock_file_cache_store(obj, file_path, file_name):
        return {"success": True,
                "file_key": "file:file_name"}

    def mock_index_cache_update_uploaded(obj, file_name):
        return {"success": True}

    def mock_publish(obj, msg_body):
        return {"message_published": True}

    mocker.patch.object(FileCache, 'store', new=mock_file_cache_store)
    mocker.patch.object(IndexCache, 'update_uploaded',
                        new=mock_index_cache_update_uploaded)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    file_cache = FileCache(test_redis_config)
    index_cache = IndexCache(test_redis_config)
    user_queue_manager = RabbitMQManager(test_user_rabbitmq_config)
    admin_queue_manager = RabbitMQManager(test_admin_rabbitmq_config)
    svc = file_uploader_service.FileUploader(file_cache, None, user_queue_manager,
                                             admin_queue_manager, index_cache)

    result = svc.delete_uploaded_file("file1", user_id, user_name)
    assert result["success"] == True


def test_handle_failed_upload(mocker):
    user_id = "user-1"
    user_name = "hello123"
    file_name = "file-3"
    max_attempts = 3

    """
    failure : index cache not responsive
    """
    def mock_index_cache_update_retry(obj, file_name, max_attempts):
        return {"success": False,
                "error": "some_error from redis"}

    mocker.patch.object(IndexCache, 'update_retry',
                        new=mock_index_cache_update_retry)

    index_cache = IndexCache(test_redis_config)
    svc = file_uploader_service.FileUploader(
        None, None, None, None, index_cache)

    result = svc.handle_failed_upload(file_name, user_id, user_name)
    assert result["success"] == False
    assert result["error"] == "Error while retrying file upload : some_error from redis"

    """
    failure : max attempts reached
    """
    def mock_index_cache_update_retry(obj, file_name, max_attempts):
        return {"success": False,
                "error": ERROR_MAX_ATTEMPTS_REACHED}

    def mock_file_cache_delete(obj, file_name):
        return {"success": True,
                "file_key": "file:file-3"}

    def mock_publish(obj, msg_body):
        return {"message_published": True}

    mocker.patch.object(IndexCache, 'update_retry',
                        new=mock_index_cache_update_retry)
    mocker.patch.object(FileCache, 'delete', new=mock_file_cache_delete)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    index_cache = IndexCache(test_redis_config)
    file_cache = FileCache(test_redis_config)
    user_queue_manager = RabbitMQManager(test_user_rabbitmq_config)
    admin_queue_manager = RabbitMQManager(test_admin_rabbitmq_config)
    svc = file_uploader_service.FileUploader(file_cache, None, user_queue_manager,
                                             admin_queue_manager, index_cache)

    result = svc.handle_failed_upload(file_name, user_id, user_name)
    assert result["success"] == False
    assert result["error"] == ERROR_MAX_ATTEMPTS_REACHED

    """
    failure : max attempts reached, failed to publish to user notification queue
    """
    def mock_index_cache_update_retry(obj, file_name, max_attempts):
        return {"success": False,
                "error": ERROR_MAX_ATTEMPTS_REACHED}

    def mock_file_cache_delete(obj, file_name):
        return {"success": True,
                "file_key": "file:file-3"}

    def mock_publish(obj, msg_body):
        return {"message_published": False,
                "error": "some error from rabbitmq"}

    mocker.patch.object(IndexCache, 'update_retry',
                        new=mock_index_cache_update_retry)
    mocker.patch.object(FileCache, 'delete', new=mock_file_cache_delete)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    index_cache = IndexCache(test_redis_config)
    file_cache = FileCache(test_redis_config)
    user_queue_manager = RabbitMQManager(test_user_rabbitmq_config)
    admin_queue_manager = RabbitMQManager(test_admin_rabbitmq_config)
    svc = file_uploader_service.FileUploader(file_cache, None, user_queue_manager,
                                             admin_queue_manager, index_cache)

    result = svc.handle_failed_upload(file_name, user_id, user_name)
    assert result["success"] == False
    assert result["error"] == "Error while retrying file upload : Error while publishing message to user notification queue : some error from rabbitmq"

    """
    failure : failed to publish file upload retry rabbitmq event
    """
    def mock_index_cache_update_retry(obj, file_name, max_attempts):
        return {"success": True,
                "metadata": "some json data"}

    def mock_publish(obj, msg_body):
        return {"message_published": False,
                "error": "something failing"}

    mocker.patch.object(IndexCache, 'update_retry',
                        new=mock_index_cache_update_retry)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    index_cache = IndexCache(test_redis_config)
    file_cache = FileCache(test_redis_config)
    file_queue_manager = RabbitMQManager(test_file_rabbitmq_config)
    svc = file_uploader_service.FileUploader(
        file_cache, file_queue_manager, None, None, index_cache)

    result = svc.handle_failed_upload(file_name, user_id, user_name)
    assert result["success"] == False
    assert result["error"] == "Error while retrying file upload : Error while publishing to file upload queue : something failing"

    """
    success
    """
    def mock_index_cache_update_retry(obj, file_name, max_attempts):
        return {"success": True,
                "metadata": "some json data"}

    def mock_publish(obj, msg_body):
        return {"message_published": True}

    mocker.patch.object(IndexCache, 'update_retry',
                        new=mock_index_cache_update_retry)
    mocker.patch.object(RabbitMQManager, 'publish', new=mock_publish)

    index_cache = IndexCache(test_redis_config)
    file_cache = FileCache(test_redis_config)
    file_queue_manager = RabbitMQManager(test_file_rabbitmq_config)
    svc = file_uploader_service.FileUploader(
        file_cache, file_queue_manager, None, None, index_cache)

    result = svc.handle_failed_upload(file_name, user_id, user_name)
    assert result["success"] == True
