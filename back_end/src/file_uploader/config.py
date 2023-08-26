import os
import pathlib
import json

INSIDE_CONTAINER = os.environ.get('IN_CONTAINER_FLAG', False)

if INSIDE_CONTAINER:
    config = json.load(open('./config_docker.json'))
    config["file_temp_upload_path"] = "tmp/"

else:
    config = json.load(open('./config_local.json'))
    config["file_temp_upload_path"] = os.path.abspath(
        pathlib.Path().absolute()) + '/'

if not os.path.exists(config["file_temp_upload_path"]):
    os.makedirs(config["file_temp_upload_path"])
