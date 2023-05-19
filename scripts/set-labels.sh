# Exit on error, we want to fail on first error.
set -e

branch=$(git branch --show-current)
author=$(git show -s --format='%aL' HEAD)
sha=$(git show -s --format='%h' HEAD)
msg=$(git show -s --format='%s' HEAD)
