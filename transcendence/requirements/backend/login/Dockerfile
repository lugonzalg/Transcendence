FROM python:alpine3.18

RUN apk add bash

COPY ./tools/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./tools/docker-entrypoint.sh docker-entrypoint.sh