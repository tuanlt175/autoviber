import yaml
from viber_bot.config import BOT_CONFIG_FILE_NAME
import unicodedata as ud
import time
import re


def remove_accents(s):
    s = re.sub("Đ", "D", s)
    s = re.sub("đ", "d", s)
    s = ud.normalize("NFKD", s).encode("ASCII", "ignore").decode("utf-8")
    return s


def get_bot_config():
    timeout = 60
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            raise IOError(f"Đang có tiến trình khác mở {BOT_CONFIG_FILE_NAME}, do đó Viberbot không thể mở file để đọc")
        try:
            with open(BOT_CONFIG_FILE_NAME, "r", encoding="utf8") as file:
                bot_config = yaml.safe_load(file)
            return bot_config
        except:
            pass


def save_new_bot_config(bot_config):
    for bot_uri, botinfor in bot_config.items():
        if "subscribers" in botinfor:
            for userid, username in botinfor["subscribers"].items():
                bot_config[bot_uri]["subscribers"][userid] = remove_accents(username)

    with open(BOT_CONFIG_FILE_NAME, "w") as file:
        yaml.dump(bot_config, file)
    return
