# RUN apt-get update && apt-get install --yes curl git wget unzip
FROM python:3.13-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

