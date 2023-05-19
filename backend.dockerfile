# Image name: demo-tpl-py
# Build context: ./

ARG BASE_TAG=local

FROM demo-tpl-py-base:$BASE_TAG

ARG VERSION=x.y.z
ENV VERSION=$VERSION

COPY --chown=1001:0 src/app ./app
COPY --chown=1001:0 src/run_server.py .
COPY --chown=1001:0 scripts ./scripts

ENV PYTHONPATH="$DIR_APP:$PYTHONPATH"

ENV PORT=8080
EXPOSE $PORT

# Run the start script, it will check for an $DIR_APP/prestart.sh script
# (e.g. for migrations). Then starts uvicorn.
CMD ["/bin/bash", "./scripts/start.sh"]