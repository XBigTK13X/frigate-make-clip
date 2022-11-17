#! /bin/bash

FMC_DEBUG=""

if [ ! -z $1 ]; then
    FMC_DEBUG='--debug'
fi

python3 -m flask --app source/server $FMC_DEBUG run --host 0.0.0.0 --port 8765