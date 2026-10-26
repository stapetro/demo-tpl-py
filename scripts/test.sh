#!/usr/bin/env bash

. $(dirname $0)/env_config.sh

uv run --locked pytest -v ./tests "${@}"
