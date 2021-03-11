.PHONY: help

# Install python dependencies.
init:
	scripts/init.sh

# Format codebase.
format:
	scripts/format.sh

# Run static code analysis (linters).
check:
	scripts/check.sh

# Run tests and check for the required coverage threshold.
test: check
	scripts/test-cov.sh

# Run tests and generate html coverage report.
coverage: check
	scripts/test-cov-html.sh

# Build docker image.
docker-build:
	scripts/docker-build.sh

# Build base docker image for dev purposes.
docker-build-base:
	scripts/docker-build-base.sh

# Build the backend inside a docker container.
docker-run:
	scripts/docker-run.sh

# Check the codebase inside a docker container.
docker-check: docker-build-base
	scripts/docker-check.sh

# Run all build steps.
build-all: init check coverage

# Run a development server.
run:
	poetry run python src/run_dev_server.py

# Show this help.
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t
