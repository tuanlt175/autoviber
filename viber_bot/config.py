from viber_bot import get_parent_root_path
import os
import yaml

service_config_file_name = os.path.join(get_parent_root_path(), "data/service_config.yml")
with open(service_config_file_name, "r") as file:
    config = yaml.safe_load(file)

BOT_CONFIG_FILE_NAME = os.path.join(get_parent_root_path(), "data/bot_config.yml")
with open(BOT_CONFIG_FILE_NAME, "r") as file:
    BOT_CONFIG = yaml.safe_load(file)

# File chứa nội dung tin nhắn mà bot sẽ gửi đi
TXT_DATA_FILE_PATH = os.path.join(get_parent_root_path(), "data", config.get("TXT_DATA_FILE_PATH"))

WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or config["WEBHOOK_URL"]

# Redis keys
USERS_FOR_BOT = os.environ.get("USERS_FOR_BOT") or config["USERS_FOR_BOT"]

# Redis config
INTERNAL_REDIS_HOST = os.environ.get("INTERNAL_REDIS_HOST") or config["INTERNAL_REDIS_HOST"]
INTERNAL_REDIS_PORT = os.environ.get("INTERNAL_REDIS_PORT") or config["INTERNAL_REDIS_PORT"]
INTERNAL_REDIS_DB = os.environ.get("INTERNAL_REDIS_DB") or config["INTERNAL_REDIS_DB"]
INTERNAL_REDIS_PW = os.environ.get("INTERNAL_REDIS_PW") or config["INTERNAL_REDIS_PW"]


# init config
SERVICE_PORT = os.environ.get("SERVICE_PORT") or config["SERVICE_PORT"]
SERVICE_HOST = os.environ.get("SERVICE_HOST") or config["SERVICE_HOST"]
WORKERS = os.environ.get("WORKERS") or config["WORKERS"] or 1
WORKERS = int(WORKERS)
SEND_MESSAGE_ITER_TIME = os.environ.get("SEND_MESSAGE_ITER_TIME") or config["SEND_MESSAGE_ITER_TIME"]
SEND_MESSAGE_ITER_TIME = int(SEND_MESSAGE_ITER_TIME)
