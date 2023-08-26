import json
import os

INSIDE_CONTAINER = os.environ.get('IN_CONTAINER_FLAG', False)


if INSIDE_CONTAINER:
     config = json.load(open('config_docker.json'))
else:
     config = json.load(open("config_local.json"))
