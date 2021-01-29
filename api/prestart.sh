#!/bin/bash

# Let DB start
sleep 5;

echo "Running alembic migrations ..."
alembic upgrade head
