#!/bin/bash

docker compose down -v
docker compose build
docker compose run duke-cli "$@"
