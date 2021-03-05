#!/bin/sh -ex

bash scripts/test-cov.sh --cov-report=html "${@}"
