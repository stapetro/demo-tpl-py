#!/bin/sh -ex

docker build -f backend.dockerfile -t demo-tpl-py . || exit $?
