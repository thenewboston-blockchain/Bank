#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE thenewboston_cv1;
    CREATE DATABASE thenewboston_cv2;
    CREATE DATABASE thenewboston_bank;
    GRANT ALL PRIVILEGES ON DATABASE thenewboston_cv1 TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE thenewboston_cv2 TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE thenewboston_bank TO $POSTGRES_USER;
EOSQL
