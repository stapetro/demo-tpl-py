#!/usr/bin/env bash

docker container stop demo-tpl-py-svc 2>/dev/null
docker container rm demo-tpl-py-svc 2>/dev/null
docker run -d --rm \
    -e PORT=8080 \
    -p 8887:8080 \
    --env-file src/.env \
    --name demo-tpl-py-svc \
    demo-tpl-py:local
