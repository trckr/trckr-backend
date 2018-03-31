#!/bin/bash

set -e

cmd="$@"

while ! curl --silent --output /dev/null  --head --fail db:5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd

