#!/usr/bin/env bash

. $(dirname $0)/env_config.sh

$POETRY_OR_NOT pytest -v ./tests "${@}"
