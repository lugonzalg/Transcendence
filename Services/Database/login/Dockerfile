FROM postgres:12.17-alpine3.19

#Estos archivos creo que hay que modificarles algo (ver docu) pero de momento no da problemas sin ellos
#COPY postgresql.conf /usr/share/postgresql/postgresql.conf
#COPY pg_hba.conf /usr/share/postgresql/postgresql.conf

COPY create_tables.sql docker-entrypoint-initdb.d/create_tables.sql

CMD ["postgres"] 