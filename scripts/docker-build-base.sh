#!/bin/bash
set -e
set -x

docker build -f ./backend_base.dockerfile -t demo-tpl-py-base . || exit $?
