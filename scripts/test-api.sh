#!/usr/bin/env bash

set -e
set -x

bash scripts/test.sh -m "api" "${@}"