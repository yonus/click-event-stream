FROM bitnami/spark:3-debian-10
USER root
RUN apt-get update && apt-get install -y cron
WORKDIR /app
COPY ./src .
RUN chmod +x ./submit.sh ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh