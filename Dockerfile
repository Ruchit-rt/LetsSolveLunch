# Dockerfile

# maven base image
FROM python:3.9-buster

CMD python3 manage.py runserver 9000

# WORKDIR /app
# COPY . /app/

# RUN apt-get update
# RUN apt-get install texlive-latex-extra pandoc -y
# RUN export PORT=5000
# RUN mvn package

# CMD sh target/bin/simplewebapp
