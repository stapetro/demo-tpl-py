#!/bin/sh -ex

sh scripts/test-cov.sh --cov-report=html "${@}"
