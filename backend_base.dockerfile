# Image name: demo-tpl-py-base
# Build context: ./
FROM debian:bookworm-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /uvx /usr/local/bin/

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

ENV DIR_HOME=/non-root
ENV DIR_APP=${DIR_HOME}/app
ENV PATH="$DIR_APP/.venv/bin:$DIR_HOME/.local/bin:$PATH"
ENV UV_PYTHON_PREFERENCE=only-managed \
    UV_LINK_MODE=copy

RUN useradd -s /bin/bash -u 1001 -g root -m -d "$DIR_HOME" non-root

USER 1001:0

SHELL ["/bin/bash", "-c"]

WORKDIR $DIR_APP

COPY --chown=1001:0 . .

RUN uv python install && uv sync --locked --no-dev

# Enable it to be used as a remote interpreter in IDE
# https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html#4e306fb5
CMD [ "python" ]
