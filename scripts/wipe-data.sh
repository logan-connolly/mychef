#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PARENTDIR="$(dirname "$DIR")"

drop_services() {
  echo "Stopping services and removing volumnes..."
  docker-compose -f ${PARENTDIR}/docker-compose.dev.yml down -v
}
drop_meilisearch() {
  echo "Removing meilisearch data.ms store [password required]  ..."
  sudo rm -rf ${PARENTDIR}/search/data.ms
}
start_services() {
  echo "Restarting services with no data ..."
  docker-compose -f ${PARENTDIR}/docker-compose.dev.yml up -d ui
}

drop_services && start_services
