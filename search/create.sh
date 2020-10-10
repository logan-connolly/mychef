#!/bin/bash

curl -X POST 'http://localhost:7700/indexes' \
  --data '{"uid" : "recipes"}'
