#!/bin/bash

service postfix start || { echo "Error al iniciar Postfix"; exit 1; }

sleep 5

echo "Enviando correo electrónico de aviso a los administradores"
/usr/local/bin/start.expect || { echo "Error al enviar el correo electrónico"; exit 1; }

service postfix stop || { echo "Error al detener Postfix"; exit 1; }
postfix start-fg || { echo "Error al iniciar Postfix en primer plano"; exit 1; }

