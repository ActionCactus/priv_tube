FROM python:3.8.7-slim

COPY . /app
WORKDIR /app
RUN pip install gunicorn
RUN pip install -r requirements.txt
