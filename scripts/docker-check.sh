#!/usr/bin/env bash

. $(dirname $0)/set-labels.sh

docker build -f ./backend_build_check.dockerfile \
	--label "git.branch=$branch" \
	--label "git.author=$author" \
	--label "git.commit.sha=$sha" \
	--label "git.commit.msg=$msg" \
	--build-arg BASE_TAG=local \
	-t dummy/demo-tpl-py-check:local .
