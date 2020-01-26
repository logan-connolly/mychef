#!/bin/bash

GUNICORN=/venv/bin/gunicorn
CONF=$PWD/mychef_scraper/config/gunicorn_conf.py
$GUNICORN app:api --chdir mychef_scraper -c $CONF --reload
