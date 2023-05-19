#!/usr/bin/env bash

. $(dirname $0)/set-labels.sh
BASE_TAG="$1"

if [ -z "$BASE_TAG" ]
then
  echo "BASE_TAG has no provided value."
  exit 1
fi

docker build -f ./backend_dev.dockerfile \
	--label "git.branch=$branch" \
	--label "git.author=$author" \
	--label "git.commit.sha=$sha" \
	--label "git.commit.msg=$msg" \
	--build-arg BASE_TAG="$BASE_TAG" \
	-t demo-tpl-py-dev:local .
