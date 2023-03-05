from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viber_bot.config import (
    SERVICE_HOST,
    SERVICE_PORT
)
from viber_bot import get_bot_config, save_new_bot_config
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


app = Flask(__name__)

BOT_CONFIG = get_bot_config()
all_vibers = {
    bot_uri: Api(BotConfiguration(
        name=bconfig["name"],
        avatar=bconfig["avatar"],
        auth_token=bconfig["auth_token"]
    )) for bot_uri, bconfig in BOT_CONFIG.items()
}


def save_subscriber(bot_uri, user_id):
    if "subscribers" not in BOT_CONFIG[bot_uri]:
        BOT_CONFIG[bot_uri]["subscribers"] = {}
    if user_id not in BOT_CONFIG[bot_uri]["subscribers"]:
        user_data = all_vibers[bot_uri].get_user_details(user_id)
        if isinstance(user_data, dict) and "name" in user_data:
            BOT_CONFIG[bot_uri]["subscribers"][user_id] = user_data["name"]
        else:
            BOT_CONFIG[bot_uri]["subscribers"][user_id] = ""
        save_new_bot_config(BOT_CONFIG)
    return


@app.route('/<bot_uri>', methods=['POST'])
def incoming(bot_uri):
    viber = all_vibers[bot_uri]

    logger.info(f"Received request - post data: {request.get_data()}")
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            TextMessage(text="Bạn vừa đăng ký nhận thông báo Bot thành công!")
        ])
        save_subscriber(bot_uri, viber_request.sender.id)

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="Bạn vừa đăng ký nhận thông báo từ Bot thành công!")
        ])
        save_subscriber(bot_uri, viber_request.get_user.id)

    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn(f"Client failed receiving message - failure: {viber_request}")

    return Response(status=200)


if __name__ == "__main__":
    app.run(host=str(SERVICE_HOST), port=int(SERVICE_PORT))
