#!/bin/bash

TAG=panel_sense
USE_DOCKER=false

for arg in "$@"; do
 case $arg in
   --docker)
     USE_DOCKER=true
     ;;
   *)
     TAG="$arg"
     ;;
  esac
done


if [ "$USE_DOCKER" = "true" ]; then
  docker build -t panel_sense .
  docker run -p 8652:8652 panel_sense
else
  ./start.sh
fi

