#!/usr/bin/env bash

# This script is executed inside the container ONLY.

# Exit on error, we want to fail the build on first error.
set -e

cd "$DIR_APP"

# look for prestart, if found execute IN-PROCESS.
if [[ -f scripts/prestart.sh ]]; then
  echo "Found prestart.sh, executing ..."
  . scripts/prestart.sh
else
  echo "No prestart.sh script found."
fi

# PORT is injected at runtime.
# add $RUN_SERVER_OPTS which could contain a "--reload" or other configuration options.
echo "Starting server ..."
poetry run python3 run_server.py --port ${PORT:-8080} $RUN_SERVER_OPTS
