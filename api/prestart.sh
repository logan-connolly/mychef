#!/bin/bash

# Let DB start
sleep 5;

echo "Running alembic migrations ..."
alembic upgrade head

echo "Instantiating meilisearch index ..."
curl -X POST "http://${SEARCH_HOST}:${SEARCH_PORT}/indexes" --data '{"uid": "recipes"}'
