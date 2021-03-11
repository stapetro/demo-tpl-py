#!/bin/sh -ex

#autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
scripts/format_common.sh src tests
