FROM haproxy:alpine3.19

RUN mkdir -p certs

COPY conf/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY certs/trascendence.tech.pem /certs/trascendence.tech.pem