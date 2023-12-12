#!/bin/bash

TAG=panel_sense
USE_DOCKER=false
FLAGS=()

for arg in "$@"; do
 case $arg in
   --docker)
     USE_DOCKER=true
     ;;
   --debug)
      FLAGS+=(--debug)
      ;;
   --mock)
      FLAGS+=(--mock)
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
  python panelsense/senseapp/sense.py "${FLAGS[@]}"
fi
