#!/bin/bash

if [ -f "/proc/1/cgroup" ]; then
    echo "Running in a docker container"
else
    echo "Running locally. Sourcing env vars"
    set -a
    source .env
    set +a
fi

cd src && poetry run -vvv python app.py
