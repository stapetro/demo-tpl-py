#!/bin/sh -ex

sh scripts/test-unit.sh --cov-config=./pyproject.toml \
  --cov=./src --cov-branch --cov-fail-under=80 "${@}"
