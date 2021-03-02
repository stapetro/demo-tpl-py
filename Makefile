test: check
	scripts/test-cov.sh

init:
	CI/init.sh

check:
	scripts/check.sh

coverage: check
	scripts/test-cov-html.sh

deploy: test
	CI/deploy.sh

run:
	uvicorn app.main:app --reload
