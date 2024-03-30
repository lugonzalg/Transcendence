FROM haproxy:alpine3.19

ARG CERT
ARG DOMAIN
ARG WWWDOMAIN

RUN mkdir -p certs

COPY conf/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY certs/${CERT} /certs/${CERT}

ENV CERT=${CERT}
ENV DOMAIN=${DOMAIN}
ENV WWWDOMAIN=${WWWDOMAIN}