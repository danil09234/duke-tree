#!/bin/bash

docker compose build

volumes=()
env_vars=()

if [ -f .env ]; then
  while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" == \#* ]] && continue
    env_vars+=("-e" "$key=$value")
  done < .env
fi

for arg in "$@"; do
  if [ -f "$arg" ]; then
    host_dir=$(dirname "$(realpath "$arg")")
    volumes+=("-v" "${host_dir}:${host_dir}:rw")
  fi
done

docker compose run "${env_vars[@]}" "${volumes[@]}" duke-cli "$@"