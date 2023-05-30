# Dockerfile

# python base image
FROM python:3.9-buster

WORKDIR /app
COPY . /app/

# RUN cd /letssolvelunch/
RUN pip install -r requirements.txt

CMD python3 manage.py runserver $PORT
