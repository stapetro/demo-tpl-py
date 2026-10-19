#!/usr/bin/env bash

. $(dirname $0)/env_config.sh

if [[ $CHECK_ONLY ]]; then
  CHECK_ONLY="--check"
else
  CHECK_ONLY=""
fi

uv run --locked autoflake $CHECK_ONLY \
  --remove-all-unused-imports --expand-star-imports --remove-duplicate-keys \
  --recursive --remove-unused-variables --ignore-init-module-imports \
  --in-place \
  --exclude=__init__.py \
  "${@}"
uv run --locked isort $CHECK_ONLY \
  --settings-file=./pyproject.toml \
  "${@}"
uv run --locked black $CHECK_ONLY \
  --config=./pyproject.toml \
  "${@}"
