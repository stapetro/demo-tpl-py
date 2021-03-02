#!/usr/bin/env bash

set -e
set -x

bash scripts/test-unit.sh --cov-config=./pyproject.toml \
  --cov=./src --cov-branch --cov-fail-under=80 "${@}"
