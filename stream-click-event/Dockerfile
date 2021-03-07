FROM bitnami/spark:3-debian-10
WORKDIR /app
COPY ./src .
USER root
RUN ["chmod", "+x", "submit.sh"]
CMD ./submit.sh