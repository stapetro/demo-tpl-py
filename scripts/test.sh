#!/bin/sh -ex

. ./scripts/env_config.sh

export PYTHONPATH=$PYTHONPATH${path_separator}src${path_separator}tests
poetry run pytest -v ./tests "${@}" || exit $?
