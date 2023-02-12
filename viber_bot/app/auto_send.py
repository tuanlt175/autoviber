from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viber_bot.config import (
    BOT_CONFIG,
    INTERNAL_REDIS_HOST,
    INTERNAL_REDIS_PORT,
    INTERNAL_REDIS_DB,
    INTERNAL_REDIS_PW,
    USERS_FOR_BOT,
    SEND_MESSAGE_ITER_TIME,
    BOT_CONFIG_FILE_NAME,
    TXT_DATA_FILE_PATH,
)
import yaml
import msgpack
import time
import logging
import redis

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


all_vibers = {
    bot_uri: Api(BotConfiguration(
        name=bconfig["name"],
        avatar=bconfig["avatar"],
        auth_token=bconfig["auth_token"]
    )) for bot_uri, bconfig in BOT_CONFIG.items()
}


INTERNAL_REDIS_CLIENT = redis.Redis(
    host=INTERNAL_REDIS_HOST,
    port=int(INTERNAL_REDIS_PORT),
    db=int(INTERNAL_REDIS_DB),
    password=INTERNAL_REDIS_PW,
)


def read_data():
    with open(TXT_DATA_FILE_PATH, "r") as file:
        data = file.read().strip()
    return data


def get_bot_info(viberx):
    key = USERS_FOR_BOT + viberx._bot_configuration.auth_token
    bot_info = msgpack.loads(INTERNAL_REDIS_CLIENT.get(key), encoding="utf-8")
    return bot_info


def save_new_bot_config(bot_config):
    with open(BOT_CONFIG_FILE_NAME, "w") as file:
        yaml.dump(bot_config, file)
    return


old_bot_config = BOT_CONFIG
time.sleep(2)
while True:
    data = read_data()
    new_bot_config = {}
    for bot_uri, viber in all_vibers.items():
        bot_info = get_bot_info(viber)
        unames = []
        for user_id, user_name in bot_info["subscribers"].items():
            viber.send_messages(user_id, [TextMessage(text=data)])
            unames.append(user_name)

        logger.info(bot_info["name"] + "vừa gửi message '" + data + "' cho " + "; ".join(unames))
        new_bot_config[bot_uri] = bot_info

    # Các thông tin subscribers mới của các bot được cập nhật thường xuyên vào file data/bot_config.yml
    if old_bot_config != new_bot_config:
        save_new_bot_config(new_bot_config)
        old_bot_config = new_bot_config

    time.sleep(SEND_MESSAGE_ITER_TIME)
