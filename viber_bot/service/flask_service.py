from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viber_bot.config import (
    BOT_CONFIG,
    SERVICE_HOST,
    SERVICE_PORT,
    INTERNAL_REDIS_HOST,
    INTERNAL_REDIS_PORT,
    INTERNAL_REDIS_DB,
    INTERNAL_REDIS_PW,
    USERS_FOR_BOT
)
import msgpack
import logging
import redis


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


app = Flask(__name__)

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
for bot_uri, viber in all_vibers.items():
    INTERNAL_REDIS_CLIENT.set(
        USERS_FOR_BOT + viber._bot_configuration.auth_token,
        msgpack.dumps({
            "auth_token": viber._bot_configuration.auth_token,
            "name": viber._bot_configuration.name,
            "avatar": viber._bot_configuration.avatar,
            "subscribers": BOT_CONFIG[bot_uri].get("subscribers", {})
        })
    )


def save_subscriber(viberx, user_id):
    key = USERS_FOR_BOT + viberx._bot_configuration.auth_token
    bot_info = msgpack.loads(INTERNAL_REDIS_CLIENT.get(key), encoding="utf-8")
    if user_id not in bot_info["subscribers"]:
        user_data = viberx.get_user_details(user_id)
        if isinstance(user_data, dict) and "name" in user_data:
            bot_info["subscribers"][user_id] = user_data["name"]
        else:
            bot_info["subscribers"][user_id] = ""
        INTERNAL_REDIS_CLIENT.mset({key: msgpack.dumps(bot_info)})
    logger.info("User " + bot_info["subscribers"][user_id] + " đã đăng ký bot " + bot_info["name"])
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
            TextMessage(text="Bạn vừa đăng ký nhận tin nhắn từ Bot thành công!")
        ])
        save_subscriber(viber, viber_request.sender.id)

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="Bạn vừa đăng ký nhận tin nhắn từ Bot thành công!")
        ])
        save_subscriber(viber, viber_request.get_user.id)

    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn(f"Client failed receiving message - failure: {viber_request}")

    return Response(status=200)


if __name__ == "__main__":
    app.run(host=str(SERVICE_HOST), port=int(SERVICE_PORT))
