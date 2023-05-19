#!/usr/bin/env bash

. $(dirname $0)/env_config.sh

if [[ $CHECK_ONLY ]]; then
  CHECK_ONLY="--check"
else
  CHECK_ONLY=""
fi

$POETRY_OR_NOT autoflake $CHECK_ONLY \
  --remove-all-unused-imports \
  --recursive --remove-unused-variables \
  --in-place \
  --exclude=__init__.py \
  "${@}"
$POETRY_OR_NOT isort $CHECK_ONLY \
  --settings-file=./pyproject.toml \
  "${@}"
$POETRY_OR_NOT black $CHECK_ONLY \
  --config=./pyproject.toml \
  "${@}"
