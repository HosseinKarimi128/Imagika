FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=contlika.settings
ENV PYTHONUNBUFFERED=1
RUN python manage.py collectstatic --no-input
EXPOSE 8000
CMD ["uvicorn", "contlika.asgi:application", "--host", "0.0.0.0", "--port", "8000"]