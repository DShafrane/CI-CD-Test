FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc musl-dev \
    && apk add postgresql-dev && \
    apk add netcat-openbsd

ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_APP="/usr/src/app/app.py"
ENV FLASK_ENV="development"
ENV FLASK_RUN_PORT="8000"

RUN mkdir /usr/src/app/
COPY . /usr/src/app/

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src/app/

CMD ["flask", "run"]
