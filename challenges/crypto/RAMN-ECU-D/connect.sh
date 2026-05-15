#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 HOST PORT" >&2
    exit 1
fi

HOST="$1"
PORT="$2"

cd connect
docker build -t canproxy-client .

docker run --rm -it \
    --cap-add NET_ADMIN \
    -e CANPROXY_SERVER_HOST="$HOST" \
    -e CANPROXY_SERVER_PORT="$PORT" \
    canproxy-client
