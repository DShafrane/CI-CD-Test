FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc musl-dev \
    && apk add postgresql-dev && \
    apk add netcat-openbsd

ENV FLASK_APP="app.py"
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_ENV="docker"

RUN mkdir -p /usr/src/app
COPY . /usr/src/app/
WORKDIR /usr/src/app/

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

EXPOSE 5000
