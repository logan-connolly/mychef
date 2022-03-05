#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PARENTDIR="$(dirname "$DIR")"

INGRED_IMAGE=lvconnolly/mychef_model:ingredient
INGRED_CONTAINER=tmp_ingred
INGRED_PATH=$PARENTDIR/backend/api/app/services/ingredient

create_tmp_containers() {
  echo "Pulling images from registry and starting temp containers ..."
  docker create -it --name $INGRED_CONTAINER $INGRED_IMAGE sh
}
copy_models() {
  echo "Pulling images from registry and starting temp containers ..."
  docker cp $INGRED_CONTAINER:/version $INGRED_PATH
}
remove_tmp_containers() {
  echo "Dropping temp containers ..."
  docker rm -f $INGRED_CONTAINER
}

create_tmp_containers && copy_models && remove_tmp_containers
