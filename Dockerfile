# Dockerfile

# python base image
FROM python:3.10-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
COPY ./requirements.txt .
# RUN cd letssolvelunch/
RUN pip install -r requirements.txt

# copy project
COPY . .

# run gunicorn
CMD gunicorn drp.wsgi:application --bind 0.0.0.0:$PORT