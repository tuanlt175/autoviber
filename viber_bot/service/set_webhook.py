from viber_bot.config import BOT_CONFIG, WEBHOOK_URL
import requests
import time


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


if __name__ == "__main__":
    time.sleep(3)
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
