FROM python:alpine3.18

RUN apk add --update bash sudo build-base libpq-dev curl

COPY tools/docker-entrypoint.sh docker-entrypoint.sh

COPY tools/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copiar el script de entrada y establecer permisos de ejecución
COPY ./tools/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ARG ADMIN=transcendence

# VARIABLES DE ENTORNO DESDE VAULT -Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
RUN mkdir secrets 
#Secrets 'login'



 

# add new user
RUN adduser -D -s /bin/bash $ADMIN \
        && mkdir -p /etc/sudoers.d \
        && echo "$ADMIN ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$ADMIN \
        && chmod 0440 /etc/sudoers.d/$ADMIN

USER $ADMIN

ENTRYPOINT [ "./docker-entrypoint.sh" ]
