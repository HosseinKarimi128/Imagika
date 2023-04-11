# FROM python:3.9
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# ENV PYTHONPATH=/app
# ENV DJANGO_SETTINGS_MODULE=contlika.settings
# ENV PYTHONUNBUFFERED=1
# EXPOSE 8000
FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000
EXPOSE 8001