FROM python:3.9-alpine

RUN apk update \
    && apk add gcc musl-dev \
    && apk add postgresql-dev && \
    apk add netcat-openbsd

COPY . /usr/src/app/
WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


ENTRYPOINT FLASK_APP=/usr/src/app/app.py flask run --host=0.0.0.0 --port=8080
