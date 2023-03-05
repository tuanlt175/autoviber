#!/bin/bash 

gunicorn -c viber_bot/service/gunicorn.conf.py viber_bot.service.wsgi_service:app &
python viber_bot/app/auto_send.py
