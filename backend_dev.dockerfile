# Image name: demo-tpl-py-dev
# Build context: ./
ARG BASE_TAG=local
FROM demo-tpl-py-base:$BASE_TAG

COPY --chown=1001:0 . .

RUN poetry install --no-ansi --no-root --only=dev

# Enable it to be used as a remote interpreter in IDE
# https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html#4e306fb5
CMD [ "python" ]
