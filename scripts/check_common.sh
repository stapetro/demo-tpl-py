#!/usr/bin/env bash

# Exit on error, we want to fail on first error.
set -e

. $(dirname $0)/env_config.sh

CHECK_ONLY=1 $(dirname $0)/format_common.sh "${@}"
$POETRY_OR_NOT pylint --rcfile=./pyproject.toml --reports=y "${@}"

# Run type checks only on the main code.
# Indexed array with files in src/
declare -a SRC_FILES

for f in "${@}"; do
  # Delete everything after the first slash
  # If "src" remains, add the file to the array
  [[ ${f%%/*} == src ]] && SRC_FILES+=($f)
done

if [[ $SRC_FILES ]]; then
  $POETRY_OR_NOT mypy --config-file=./pyproject.toml "${SRC_FILES[@]}"
else
  echo "No src files to mypy."
fi
