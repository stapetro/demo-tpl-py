#!/usr/bin/env bash

REQUIRED_COVERAGE=85

scripts/test.sh \
  -m "unit" \
  --cov-config=./pyproject.toml \
  --cov=./src \
  --cov-branch \
  --cov-fail-under=${REQUIRED_COVERAGE} \
  --cov-report term-missing:skip-covered \
  "${@}"
