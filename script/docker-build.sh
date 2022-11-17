#! /bin/bash

docker build -t xbigtk13x/frigate-make-clip .

if [ ! -z $1 ]; then
  docker push xbigtk13x/frigate-make-clip
fi
