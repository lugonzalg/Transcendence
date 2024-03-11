FROM python:alpine3.18

RUN apk add --update bash sudo build-base libpq-dev libffi-dev && mkdir -p /tools

COPY ./tools/params.json /tools/params.json
COPY ./tools/logger.json /tools/logger.json
COPY ./tools/docker-entrypoint.sh docker-entrypoint.sh

COPY ./tools/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ARG ADMIN=transcendence
ARG PORT=25671

# add new user
RUN adduser -D -s /bin/bash $ADMIN \
        && mkdir -p /etc/sudoers.d \
        && echo "$ADMIN ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$ADMIN \
        && chmod 0440 /etc/sudoers.d/$ADMIN
USER $ADMIN

EXPOSE $PORT

ENTRYPOINT [ "./docker-entrypoint.sh" ]
