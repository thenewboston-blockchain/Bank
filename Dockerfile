FROM python:3.8-alpine

WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements/local.txt /requirements.txt
COPY ./thenewboston.tar.* .

RUN set -xe \
    && apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libressl-dev libffi-dev make \
    && apk add postgresql-dev \
    && apk add postgresql-client \
    && pip install --upgrade pip pip-tools \
    && pip install --no-cache-dir -r /requirements.txt \
    && if [ -f thenewboston.tar.gz ]; then pip install thenewboston.tar.gz; fi \
    && apk del build-deps \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache

COPY . .
