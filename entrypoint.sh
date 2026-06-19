#!/bin/sh

echo "Aplicando migrations..."

python manage.py migrate

echo "Coletando arquivos estáticos..."

python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."

gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000