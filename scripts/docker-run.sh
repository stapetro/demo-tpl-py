#!/bin/sh -x

docker container stop demo-tpl-py-svc; docker container rm demo-tpl-py-svc
docker run -d --rm --name demo-tpl-py-svc -p 8889:80 demo-tpl-py || exit $?
