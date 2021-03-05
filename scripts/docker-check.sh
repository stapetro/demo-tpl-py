#!/bin/sh -ex

(docker build -f ./backend_build_check.dockerfile -t demo-tpl-py-check . && \
docker run -i --rm --name demo-tpl-py-check-runtime demo-tpl-py-check) || exit $?
