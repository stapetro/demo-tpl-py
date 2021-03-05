init:
	CI/init.sh

format:
	scripts/format.sh

check:
	scripts/check.sh

test: check
	scripts/test-cov.sh

coverage: check
	scripts/test-cov-html.sh

deploy: test
	CI/deploy.sh

run:
	poetry run python src/run_dev_server.py
