#!/bin/bash

docker compose down --remove-orphans -v
docker compose build
docker compose run duke-cli "$@"
