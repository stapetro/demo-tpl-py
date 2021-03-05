#!/bin/sh

modified_py_files=$1

. ./scripts/env_config.sh

sh ./scripts/format_common.sh ${modified_py_files} || exit $?
auto_modified_files=$(git diff --name-only | grep ".*\.py$")
if [ -z "$auto_modified_files" ]
then
#    POSIX way to define an empty array
  declare -a mod_files_to_stage
else
  # Intersection between two sorted arrays
  declare -A file_count
  for file_name in $modified_py_files $auto_modified_files
  do
    if [[ -n ${file_count[$file_name]} ]] ; then
      file_count[$file_name]=$(( ${file_count[$file_name]} + 1 ))
    else
      file_count[$file_name]=1
    fi
  done
  for file_name in "${!file_count[@]}"
  do
    { [ ${file_count[$file_name]} -gt 1 ] && mod_files_to_stage+=($file_name);}
  done
fi
if [ -z "$mod_files_to_stage" ]
then
  echo "Files are formatted good. Congrats."
else
  git add $mod_files_to_stage || exit $?
fi

if [ -z "$modified_py_files" ]
then
  echo "pylint and mypy have no work to do."
else
  poetry run pylint --rcfile=./pyproject.toml ${modified_py_files} || exit $?
  modified_src_files=$(echo "${modified_py_files}" | grep "src/")
  if [ -z "$modified_src_files" ]
  then
    echo "No src files to mypy."
  else
    poetry run mypy ${modified_src_files} || exit $?
  fi
fi

sh ./scripts/test-cov.sh || exit $?
