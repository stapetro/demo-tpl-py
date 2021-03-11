#!/bin/sh -ex

scripts/test-cov.sh --cov-report=html "${@}"
