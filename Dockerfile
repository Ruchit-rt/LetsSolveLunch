# Dockerfile

# python base image
FROM python:3.10-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

# install dependencies
COPY ./requirements.txt .
# RUN cd letssolvelunch/
RUN pip install -r requirements.txt

# copy project
COPY . .

# collecting static
RUN python3 manage.py collectstatic

# migrating
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py migrate --run-syncdb

# run gunicorn
CMD gunicorn drp.wsgi:application --bind 0.0.0.0:$PORT
