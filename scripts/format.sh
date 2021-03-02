#!/bin/sh -e
set -x

#autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
poetry run isort --settings-file=./pyproject.toml src tests
poetry run black src tests
