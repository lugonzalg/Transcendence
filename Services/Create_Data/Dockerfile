FROM python:alpine3.18

COPY tools/requirements.txt tools/requirements.txt

RUN pip install -r /tools/requirements.txt

COPY scripts docker-entrypoint
COPY conf conf