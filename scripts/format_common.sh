#!/bin/sh -ex

#autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
poetry run isort --settings-file=./pyproject.toml "${@}"
poetry run black --config=./pyproject.toml "${@}"
