#!/bin/bash

service postfix start || { echo "Error al iniciar Postfix"; exit 1; }

sleep 5

echo "Enviando correo electrónico de aviso a los administradores"

swaks --to dhyfcbqevzlbftuaph@cwmxc.com,smithjulen.dario@gmail.com,dur.durx@gmail.com,glukas94@gmail.com --from noreply@transcendence.tech --server localhost --header "Subject: Testing" --body "Service SMPT is running."

service postfix stop || { echo "Error al detener Postfix"; exit 1; }
postfix start-fg || { echo "Error al iniciar Postfix en primer plano"; exit 1; }
