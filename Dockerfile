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
RUN find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
RUN find . -path "*/migrations/*.pyc"  -delete
RUN echo "from django.db.migrations.recorder import MigrationRecorder;MigrationRecorder.Migration.objects.filter(app='main').delete()" | python3 manage.py shell 
RUN python manage.py makemigrations main
RUN python manage.py migrate --fake main zero
RUN python manage.py migrate --fake

# run gunicorn
CMD gunicorn drp.asgi:application --bind 0.0.0.0:$PORT
