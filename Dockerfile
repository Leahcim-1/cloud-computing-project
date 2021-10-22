# syntax=docker/dockerfile:1

FROM python:3.7-alphine3.13
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD python3 manage.py runserver 0.0.0.0:8000