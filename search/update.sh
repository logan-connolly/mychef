#!/bin/bash

BASE=http://localhost
curl ${BASE}:8002/api/v1/sources/1/recipes/ |\
    curl -X POST ${BASE}:7700/indexes/recipes/documents --data @-
