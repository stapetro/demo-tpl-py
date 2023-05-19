export POETRY_ENABLED := 1

.PHONY: help

SHELL=bash

# Show this help.
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t

# Install python dependencies.
init:
	scripts/init.sh

# Format codebase.
format:
	scripts/format.sh

# Check the codebase on the host machine.
check:
	scripts/check.sh

# Run tests and check for the required coverage threshold.
test:
	scripts/test-cov.sh

# Run tests and generate html coverage report.
coverage:
	scripts/test-cov-html.sh

# Run all build steps.
build-all: init check coverage

# Run a development server on the host machine.
run:
	cd src && poetry run python run_server.py --port 8001 --reload "./"

# Build prod-ready docker image (lighter than dev img).
docker-build:
	scripts/docker-build-base.sh
	scripts/docker-build.sh "local"

# Run the backend inside a docker container.
docker-run:
	scripts/docker-run.sh

# Build docker image for dev activities.
docker-build-dev:
	scripts/docker-build-base.sh
	scripts/docker-build-dev.sh "local"

# Check the codebase inside a docker container.
docker-check: docker-build-dev
	scripts/docker-check.sh
