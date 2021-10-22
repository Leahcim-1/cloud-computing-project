# syntax=docker/dockerfile:1

FROM python:3.7-alpine3.13
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install ruamel.yaml==0.17.16
RUN python3 -m pip install ruamel.yaml.clib==0.2.6
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 manage.py runserver 0.0.0.0:8000