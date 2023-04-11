# FROM python:3.9
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# ENV PYTHONPATH=/app
# ENV DJANGO_SETTINGS_MODULE=contlika.settings
# ENV PYTHONUNBUFFERED=1
# EXPOSE 8000
# FROM python:3.9

# ENV PYTHONUNBUFFERED 1

# RUN mkdir /code
# WORKDIR /code

# COPY requirements.txt /code/
# RUN pip install -r requirements.txt

# COPY . /code/

# EXPOSE 8000
# EXPOSE 8001
# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .