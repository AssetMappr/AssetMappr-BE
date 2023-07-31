#!/bin/sh

# Check for env file 
ENV_FILE=.env
if [ ! -f "$ENV_FILE" ]; then
    echo "$ENV_FILE doesn't exists."
    exit 1
fi

# Stop service
docker-compose stop
# Build and start service 
docker-compose up --build --detach