FROM python:3.9-alpine

RUN apk update \
    && apk add gcc musl-dev \
    && apk add postgresql-dev && \
    apk add netcat-openbsd

ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_APP="app.py"
ENV FLASK_ENV="development"
ENV FLASK_RUN_PORT="8000"

COPY . /tmp/

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /tmp

CMD ["flask", "run"]
