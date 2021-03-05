#!/bin/sh -ex

poetry install --no-root --remove-untracked || exit $?
