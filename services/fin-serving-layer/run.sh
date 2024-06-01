#!/bin/bash

if [ -f "/proc/1/cgroup" ]; then
    echo "Running in a docker container"
else
    echo "Running locally. Sourcing env vars"
    set -a
    source .env
    set +a
fi

if [ -z "$SERVICE_HOST" ]; then
  echo "SERVICE_HOST env var is not set"
  exit 1
fi

if [ -z "$SERVICE_PORT" ]; then
  echo "SERVICE_PORT env var is not set"
  exit 1
fi

uvicorn app:app --host $SERVICE_HOST --port $SERVICE_PORT
