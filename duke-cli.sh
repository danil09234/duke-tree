#!/bin/bash

docker compose down --remove-orphans -v
docker compose build

volumes=()

for arg in "$@"; do
  if [ -f "$arg" ]; then
    host_dir=$(dirname "$(realpath "$arg")")
    volumes+=("-v" "${host_dir}:${host_dir}:ro")
  fi
done

docker compose run "${volumes[@]}" duke-cli "$@"