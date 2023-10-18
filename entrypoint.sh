#!/usr/bin/env sh
set -ex

until nc -w 1 -z hydr_db 5432; do
  >&2 echo 'Postgres is unavailable - sleeping'
  sleep 1
done
sleep 2
  >&2 echo 'Postgres is up - executing command'

alembic upgrade head
# && uvicorn app.main:app --reload --host 0.0.0.0 --port 9090