from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viber_bot.config import (
    SEND_MESSAGE_ITER_TIME,
    LOG_FOLDER,
    WEBHOOK_URL
)
from viber_bot import get_bot_config
import datetime
import time
import requests
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def set_webhook(secret_token, webhook_url):
    res = requests.post(
        url="https://chatapi.viber.com/pa/set_webhook",
        json={
            "url": webhook_url,
            "event_types": [
                "delivered",
                "seen",
                "failed",
                "subscribed",
                "unsubscribed",
                "conversation_started"
            ],
            "send_name": True,
            "send_photo": True
        },
        headers={"X-Viber-Auth-Token": secret_token}
    )
    return res


def get_text_message():
    datetimenow = str(datetime.datetime.now())
    return f"Cổng 462 mở lúc {datetimenow}"


def check_logs():
    if not os.path.isdir(LOG_FOLDER):
        assert False, f"Thư mục {LOG_FOLDER} không tồn tại!"
    if len(os.listdir(LOG_FOLDER)) > 0:
        return True
    else:
        return False


def get_bot_info(bot_uri):
    current_bot_config = get_bot_config()
    return current_bot_config[bot_uri]


if __name__ == "__main__":
    BOT_CONFIG = get_bot_config()

    # start set webhook
    time.sleep(5)
    for bot_uri, bconfig in BOT_CONFIG.items():
        webhook_url = WEBHOOK_URL + "/" + bot_uri
        try:

            res = set_webhook(bconfig["auth_token"], webhook_url)
            if res.json().get("status_message") == "ok":
                print("BOT: " + bconfig["name"] + "- set_webhook=" + webhook_url)
            else:
                print("BOT: " + bconfig["name"] + "set_webhook không thành công.")
        except:
            print("Exception - BOT: " + bconfig["name"] + "set_webhook không thành công.")
    # end set webhook

    all_vibers = {
        bot_uri: Api(BotConfiguration(
            name=bconfig["name"],
            avatar=bconfig["avatar"],
            auth_token=bconfig["auth_token"]
        )) for bot_uri, bconfig in BOT_CONFIG.items()
    }

    old_bot_config = BOT_CONFIG
    time.sleep(2)
    while True:
        data = get_text_message()
        if check_logs():
            for i in range(10):
                for bot_uri, viber in all_vibers.items():
                    bot_info = get_bot_info(bot_uri)
                    unames = []
                    for user_id, user_name in bot_info.get("subscribers", {}).items():
                        viber.send_messages(user_id, [TextMessage(text=data)])
                        unames.append(user_name)

                    logger.info(bot_info["name"] + "vừa gửi message '" + data + "' cho " + "; ".join(unames))
                time.sleep(SEND_MESSAGE_ITER_TIME * 2)
            break

        time.sleep(SEND_MESSAGE_ITER_TIME)
