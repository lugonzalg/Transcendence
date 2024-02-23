FROM ubuntu:latest

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y postfix
RUN apt-get install libsasl2-2 libsasl2-modules
RUN apt-get install -y swaks
RUN apt install -y postfix sasl2-bin

COPY ./main.cf /etc/postfix/main.cf
COPY ./start-postfix.sh /usr/local/bin/start-postfix.sh
COPY ./start-postfix.sh /usr/local/bin/start-postfix.sh

RUN chmod +x /usr/local/bin/start-postfix.sh

ENTRYPOINT ["/bin/bash", "-c", "/usr/local/bin/start-postfix.sh"]