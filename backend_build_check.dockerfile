FROM demo-tpl-py-base:latest

WORKDIR /usr/src/app

COPY ./src ./src
COPY ./tests ./tests

CMD [ "make", "test" ]
