FROM python:3.11 AS base

# ensure /etc/apt/sources.list exists and change APT source to aliyun mirror
RUN if [ -f /etc/apt/sources.list ]; then \
    sed -i 's|http://deb.debian.org/debian|http://mirrors.aliyun.com/debian|g' /etc/apt/sources.list; \
    sed -i 's|http://security.debian.org/debian-security|http://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list; \
    apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*; \
    else \
    echo "No sources.list found!"; \
    fi



# set working directory
WORKDIR /app

# set pip mirror source
# It is recommended to configure pip mirror sources within China.
# ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
# ENV PIP_TRUSTED_HOST=mirrors.aliyun.com

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt






FROM python:3.11-slim
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 复制可执行文件
COPY --from=base /usr/local/bin/flask /usr/local/bin/flask
COPY --from=base /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY app.py app.py
COPY flaskr flaskr
COPY migrations migrations
COPY prompts prompts
# declare service running on port 5800
EXPOSE 5800
# start flask service
CMD gunicorn  -k gevent -w 4 -b 0.0.0.0:5800 "app:app" --timeout 300 --log-level info --access-logfile /var/log/app.log --capture-output
