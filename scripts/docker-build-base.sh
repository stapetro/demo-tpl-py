#!/usr/bin/env bash

. $(dirname $0)/set-labels.sh

docker build -f ./backend_base.dockerfile \
	--label "git.branch=$branch" \
	--label "git.author=$author" \
	--label "git.commit.sha=$sha" \
	--label "git.commit.msg=$msg" \
	-t demo-tpl-py-base:local .
