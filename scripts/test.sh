#!/bin/sh -ex

. ./scripts/env_config.sh

poetry run pytest -v ./tests "${@}" || exit $?
