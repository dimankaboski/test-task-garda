FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential
RUN apt-get install openssl

WORKDIR /api

COPY /requirements.txt .
RUN pip install -r requirements.txt --default-timeout=100
