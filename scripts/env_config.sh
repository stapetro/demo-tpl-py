# Exit on error, we want to fail on first error.
set -e

kernelNameOut="$(uname -s)"

case "${kernelNameOut}" in
    CYGWIN*)    path_separator=";";;
     MINGW*)    path_separator=";";;
      MSYS*)    path_separator=";";;
          *)    path_separator=":";;
esac

[[ "${PYTHONPATH}" =~ "\bsrc\b" ]] || PYTHONPATH=$PYTHONPATH${path_separator}src
[[ "${PYTHONPATH}" =~ "\btests\b" ]] || PYTHONPATH=$PYTHONPATH${path_separator}tests

export PYTHONPATH

if [[ $POETRY_ENABLED ]]
then
  export POETRY_OR_NOT="poetry run"
else
  export POETRY_OR_NOT=""
fi
