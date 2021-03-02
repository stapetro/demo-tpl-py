#!/bin/sh -e
set -x

poetry run isort --settings-file=./pyproject.toml --check src tests || exit $?
poetry run black --config=./pyproject.toml --check src tests || exit $?
poetry run pylint --rcfile=./pyproject.toml --reports=y src tests || exit $?
poetry run mypy src/app || exit $?
