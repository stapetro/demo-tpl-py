#!/bin/sh -e

set -e
set -x

kernelNameOut="$(uname -s)"
case "${kernelNameOut}" in
    CYGWIN*)    path_separator=";";;
    MINGW*)     path_separator=";";;
    *)          path_separator=":";;
esac

export PYTHONPATH=$PYTHONPATH${path_separator}src${path_separator}tests
poetry run pytest -v ./tests "${@}" || exit $?
