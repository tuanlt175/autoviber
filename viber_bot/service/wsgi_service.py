from viber_bot.service.flask_service import app
from waitress import serve
from viber_bot.config import (
    SERVICE_HOST,
    SERVICE_PORT
)
if __name__ == "__main__":
    serve(app, host=SERVICE_HOST, port=int(SERVICE_PORT))
