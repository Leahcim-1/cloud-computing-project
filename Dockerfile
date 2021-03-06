# syntax=docker/dockerfile:1

FROM python:3.7-alpine3.13
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./react1 .
CMD python3 manage.py runserver 0.0.0.0:8000