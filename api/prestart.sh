#!/usr/bin/env bash

# Let DB start
sleep 10;

# Run alembic migrations
alembic upgrade head
