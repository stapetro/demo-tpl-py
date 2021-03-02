#!/bin/sh -e
set -x

poetry run isort --settings-file=./pyproject.toml --check src tests || exit $?
poetry run black --config=./pyproject.toml --check src tests || exit $?

kernelNameOut="$(uname -s)"
case "${kernelNameOut}" in
    CYGWIN*)    path_separator=";";;
    MINGW*)     path_separator=";";;
    *)          path_separator=":";;
esac

export PYTHONPATH=$PYTHONPATH${path_separator}src${path_separator}tests
poetry run pylint --rcfile=./pyproject.toml --reports=y src tests || exit $?

poetry run mypy src/app || exit $?
