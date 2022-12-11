#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DB_HOST 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py collectstatic --no-input --clear
python manage.py migrate
gunicorn payment_gateway.wsgi:application -b 0.0.0.0:8000

exec "$@"