import os
import yaml


def get_parent_root_path():
    """Trả về đường dẫn đến thư mục cha của thư mục chứa project."""
    root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return root_path


service_config_file_name = os.path.join(get_parent_root_path(), "data/service_config.yml")
with open(service_config_file_name, "r", encoding="utf8") as file:
    config = yaml.safe_load(file)

BOT_CONFIG_FILE_NAME = os.path.join(get_parent_root_path(), "data/bot_config.yml")


LOG_FOLDER = os.environ.get("WEBHOOK_URL") or config["LOG_FOLDER"]

WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or config["WEBHOOK_URL"]


# init config
SERVICE_PORT = os.environ.get("SERVICE_PORT") or config["SERVICE_PORT"]
SERVICE_HOST = os.environ.get("SERVICE_HOST") or config["SERVICE_HOST"]
WORKERS = os.environ.get("WORKERS") or config["WORKERS"] or 1
WORKERS = int(WORKERS)
SEND_MESSAGE_ITER_TIME = os.environ.get("SEND_MESSAGE_ITER_TIME") or config["SEND_MESSAGE_ITER_TIME"]
SEND_MESSAGE_ITER_TIME = int(SEND_MESSAGE_ITER_TIME)
