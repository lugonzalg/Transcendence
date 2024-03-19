#!/bin/bash

# Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
curl -k  --header "X-Vault-Token: hvs.Dd77um8uAHucsxDQwx6RQSoz"  --request GET  https://trascendence.tech:8200/v1/transcendence/data/vue >secrets.json
# Extraer las variables de entorno del archivo JSON y exportarlas
source <(awk -F '"' '/VUE_APP_GOOGLE_OAUTH_URL/{print "export VUE_APP_GOOGLE_OAUTH_URL=" $4}' secrets.json)
# Ejecutar el comando por defecto
exec "$@"
