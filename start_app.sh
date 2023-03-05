#!/bin/bash 

python viber_bot/service/wsgi_service.py &
python viber_bot/app/auto_send.py
