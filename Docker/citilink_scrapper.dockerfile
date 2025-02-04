FROM python:3.12-slim-bookworm
# RUN apt-get update && apt-get install --yes curl git wget unzip
RUN mkdir /app
WORKDIR /app
