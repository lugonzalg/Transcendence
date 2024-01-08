#!/bin/bash
set -e

# Iniciar PostgreSQL
/docker-entrypoint.sh postgres &

# Esperar a que PostgreSQL esté disponible
until pg_isready; do
  echo "Esperando a que PostgreSQL se inicie..."
  sleep 1
done

# Ejecutar pg_resetxlog
pg_resetxlog /var/lib/postgresql/data


# Ejecutar el script create_tables.sql --OJO! METER VARIABLES DE ENTORNO 
psql -U trans -d login_db -f /docker-entrypoint-initdb.d/create_tables.sql
