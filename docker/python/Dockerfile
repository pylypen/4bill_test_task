FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apt-get install default-libmysqlclient-dev
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN useradd user

USER user
