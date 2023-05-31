# Image name: dummy/demo-tpl-py-check
# Build context: ./
FROM demo-tpl-py-dev:local

COPY --chown=1001:0 . .

ENV POETRY_ENABLED=1

RUN scripts/check.sh
RUN scripts/test-cov.sh --cov-report=xml --junitxml=junit/test-results.xml
