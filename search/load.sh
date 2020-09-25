# add recipes to indices
BASE=http://localhost
curl ${BASE}:${API_PORT}/api/v1/sources/1/recipes/ |\
    curl -X POST ${BASE}:${SEARCH_PORT}/indexes/recipes/documents --data @-
