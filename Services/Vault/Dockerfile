FROM hashicorp/vault:1.15

RUN mkdir -p /cert /conf /docker-entrypoint

COPY conf /conf
COPY cert /cert
COPY scripts /docker-entrypoint

ENTRYPOINT [ "/docker-entrypoint/docker-entrypoint.sh" ]