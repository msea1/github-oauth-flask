FROM alpine:latest

RUN apk add --no-cache --update python3 py3-pip bash

ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

ADD ./src /opt/oauth/src/
ADD app.py /opt/oauth/
WORKDIR /opt/oauth

RUN adduser -D myuser
USER myuser

CMD gunicorn app:app
