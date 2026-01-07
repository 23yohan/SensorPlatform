#!/bin/sh
CONFIG_PATH=${1:-default} # use the first argument, fall back to
echo "Using config: ./config/${CONFIG_PATH}.yaml"
exec python3 main.py -c ./config/${CONFIG_PATH}.yaml