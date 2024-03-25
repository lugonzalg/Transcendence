FROM python:alpine3.18 as builder

ARG VAULT_URL
ARG VAULT_TOKEN

COPY ./tools/docker-entrypoint.sh docker-entrypoint.sh
COPY ./tools/requirements.txt ./requirements.txt

RUN apk add --update bash sudo build-base libpq-dev libffi-dev curl \
        && pip install -r requirements.txt \
        && mkdir -p secrets \
        && curl -k --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET  ${VAULT_URL}/v1/transcendence/data/login_intra > secrets/login_intra_secrets.json \
        && curl -k --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET  ${VAULT_URL}/v1/transcendence/data/login_google > secrets/login_google_secrets.json \
        && curl -k --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET  ${VAULT_URL}/v1/transcendence/data/server > secrets/server_secrets.json \
        && curl -k --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET  ${VAULT_URL}/v1/transcendence/data/logger > secrets/logger_secrets.json \
        && curl -k --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET  ${VAULT_URL}/v1/transcendence/data/postgres_db > secrets/postgres_db_secrets.json

FROM python:alpine3.18 AS runner

ARG ADMIN

EXPOSE 25671

COPY --from=builder /usr/lib/libpq.so.5 /usr/lib/libpq.so.5
COPY --from=builder /docker-entrypoint.sh /docker-entrypoint.sh
COPY --from=builder /usr/local/bin/django-admin /usr/local/bin/django-admin
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /secrets /secrets

RUN mkdir -p /app \
        && adduser -D -s /bin/bash $ADMIN \
        && chown $ADMIN:$ADMIN /app

USER $ADMIN

ENTRYPOINT [ "./docker-entrypoint.sh" ]
