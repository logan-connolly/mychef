#!/usr/bin/env bash

# Let DB start
sleep 5;

# Run alembic migrations
alembic upgrade head
