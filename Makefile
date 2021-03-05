init:
	scripts/init.sh

format:
	scripts/format.sh

check:
	scripts/check.sh

test: check
	scripts/test-cov.sh

coverage: check
	scripts/test-cov-html.sh

docker-build:
	scripts/docker-build.sh

docker-run:
	scripts/docker-run.sh

docker-check:
	scripts/docker-check.sh

build-all: init check coverage

run:
	poetry run python src/run_dev_server.py
