FROM ubuntu:22.04

ENV FLASK_APP=flaskr
ENV FLASK_ENV=development

COPY . /app

WORKDIR /app

RUN apt update && apt install python3 python3-pip curl wget git unzip -y && pip install --editable .

#
#FROM python:3.9-slim-buster
#RUN apt update -y && apt install awscli -y
#WORKDIR /app
#
#COPY . /app
#RUN pip install -r requirements.txt
#
## Ensure the model file is copied into the correct path
## COPY data/training/model.keras /app/data/training/model.keras
#
#EXPOSE 8080
#
#CMD ["python3", "app.py"]
