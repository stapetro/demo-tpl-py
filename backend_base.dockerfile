FROM python:3.8

WORKDIR /usr/src/app

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* mypy.ini Makefile ./
COPY ./scripts ./scripts
RUN sh -c "make init"

CMD [ "python" ]
