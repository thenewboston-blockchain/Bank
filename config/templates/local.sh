#!/usr/bin/env bash

export $(grep -v '^#' .env-common | xargs)
export $(grep -v '^#' .env-bank | xargs)
export $(grep -v '^#' .env | xargs)

export SECRET_KEY='<replace with some random string>'

export REDIS_HOST=127.0.0.1
export POSTGRES_HOST=127.0.0.1
