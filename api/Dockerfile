FROM python:3.8-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt . 

RUN apt-get update && apt-get install -y build-essential \
		&& pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* 

COPY . .
