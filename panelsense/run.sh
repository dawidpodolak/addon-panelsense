#!/bin/bash

TAG=panel_sense
USE_DOCKER=false
DEBUG_UI=false

for arg in "$@"; do
 case $arg in
   --docker)
     USE_DOCKER=true
     ;;
   --debugUI)
      DEBUG_UI=true
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
  if [ "$DEBUG_UI" = "true" ]; then
    python senseapp/sense.py --debugUI
  else
    python senseapp/sense.py
  fi
fi

