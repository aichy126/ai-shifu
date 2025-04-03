FROM registry.cn-beijing.aliyuncs.com/aigitlab/python:3.11-slim-base

COPY app.py app.py
COPY flaskr flaskr
COPY migrations migrations
# declare service running on port 5800
EXPOSE 5800
# start flask service
CMD gunicorn  -k gevent -w 4 -b 0.0.0.0:5800 "app:app" --timeout 300 --log-level info --access-logfile /var/log/app.log --capture-output
