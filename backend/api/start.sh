#!/bin/bash

set -e

# Export variables
MODULE_NAME=${MODULE_NAME:-app.main}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}
export GUNICORN_CONF=${GUNICORN_CONF:-./gunicorn_conf.py}

# Prestart script
sleep 5
echo "Running alembic migrations ..."
alembic upgrade head
echo "Instantiating meilisearch index ..."
curl -X POST "http://search:7700/indexes" --data '{"uid": "recipes"}'

# Start app server
if [[ $DEBUG_SERVER = true ]]; then
  exec uvicorn --reload --host 0.0.0.0 --port 8000 "$APP_MODULE"
else
  exec gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"
fi
