#!/usr/bin/env bash

set -e

uv python install
uv sync --locked
