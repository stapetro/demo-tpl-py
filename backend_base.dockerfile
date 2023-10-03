# Image name: demo-tpl-py-base
# Build context: ./
FROM python:3.11.5-bullseye

ENV DIR_HOME=/non-root
ENV DIR_APP=${DIR_HOME}/app
ENV PATH="$DIR_HOME/.local/bin:$DIR_HOME/.local/pipx/venvs/poetry/bin:$PATH"

RUN useradd -s /bin/bash -u 1001 -g root -m -d $DIR_HOME non-root

USER 1001:0

SHELL ["/bin/bash", "-c"]

# Install Poetry
RUN python -m pip install --upgrade pip==23.2.1 \
    && python -m pip install --user pipx \
    && python -m pipx ensurepath \
    && pipx install poetry==1.6.1 \
    && poetry config cache-dir $DIR_HOME/.cache/pypoetry \
    && poetry config virtualenvs.create false

WORKDIR $DIR_APP

COPY --chown=1001:0 . .

RUN poetry install --no-root --only=main

# Enable it to be used as a remote interpreter in IDE
# https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html#4e306fb5
CMD [ "python" ]
