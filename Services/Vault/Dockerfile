FROM hashicorp/vault:1.15

RUN mkdir -p /cert

COPY tools /tmp
COPY cert /cert

ENTRYPOINT [ "/tmp/docker-entrypoint.sh" ]