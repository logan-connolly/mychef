#!/bin/bash

set -e

# Export variables
export APP_MODULE=${MODULE_NAME:-app.main:app}
export GUNICORN_CONF=${GUNICORN_CONF:-gunicorn_conf.py}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# Prestart script
sleep 5
echo "Running alembic migrations ..."
alembic upgrade head

# Start app server
if [[ $ENV = "debug" ]]; then
  exec python -u -m debugpy --listen localhost:5678 -m uvicorn --host 0.0.0.0 --port 8000 "$APP_MODULE"
elif [[ $ENV = "dev" ]]; then
  exec uvicorn --reload --host 0.0.0.0 --port 8000 "$APP_MODULE"
else
  exec gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"
fi
