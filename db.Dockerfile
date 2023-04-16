FROM postgres:latest

ENV POSTGRES_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

CMD ["postgres"]