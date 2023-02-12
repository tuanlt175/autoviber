# coding=utf-8
from viber_bot.config import SERVICE_HOST, SERVICE_PORT, WORKERS

loglevel = "info"
errorlog = "-"
accesslog = "-"

# bind = 'unix:%s' % os.path.join(_VAR, 'run/gunicorn.sock')
bind = str(SERVICE_HOST) + ":" + str(SERVICE_PORT)
workers = WORKERS

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True
