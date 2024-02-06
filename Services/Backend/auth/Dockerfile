FROM python:alpine3.18

RUN apk add --update bash sudo build-base libpq-dev

COPY ./tools/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ARG ADMIN=transcendence

# add new user
RUN adduser -D -s /bin/bash $ADMIN \
        && mkdir -p /etc/sudoers.d \
        && echo "$ADMIN ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$ADMIN \
        && chmod 0440 /etc/sudoers.d/$ADMIN

USER $ADMIN

COPY ./tools/docker-entrypoint.sh docker-entrypoint.sh