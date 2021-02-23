FROM python:3.9.2-alpine

WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY pyproject.toml .
COPY poetry.lock .

RUN set -xe \
    && apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libressl-dev libffi-dev make cargo \
    && apk add postgresql-dev postgresql-client curl \
    && pip install pip==21.0.1 \
    && pip install virtualenvwrapper \
    && pip install poetry==1.1.4

# TODO(dmu) MEDIUM: Exclude development dependencies from build
RUN poetry export --without-hashes --dev -f requirements.txt -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    # TODO(dmu) HIGH: Do we still need to install `thenewboston` lib like this?
    && if [ -f ./dist/thenewboston.tar.gz ]; then pip install ./dist/thenewboston.tar.gz; fi

RUN apk del build-deps \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache

# Copy everything here for docker build optimization purposes
# We do not use just `COPY . .` to avoid accidental inclusion sensitive information from
# developers' machines into an image
COPY thenewboston_bank .
COPY config .
COPY tests .
COPY scripts .

COPY LICENSE .
COPY manage.py .
COPY pytest.ini .

# TODO(dmu) MEDIUM: Do we need to copy derictories below?
COPY logs .
COPY media .
COPY static .
