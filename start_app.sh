#!/bin/bash 

source activate viber
redis-server --port 6379 &
gunicorn -c viber_bot/service/gunicorn.conf.py viber_bot.service.wsgi_service:app &
python viber_bot/service/set_webhook.py &
python viber_bot/app/auto_send.py
