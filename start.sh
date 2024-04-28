#!/usr/bin/env bash

echo "Starting migrations"
python manage.py makemigrations migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo "Starting qcluster"
python manage.py qcluster &

echo "Starting server"
if [ "$1" = "--debug" ]; then
  python manage.py runserver 0.0.0.0:8800
else
  gunicorn "$APP_NAME.wsgi:application" \
    --bind "0.0.0.0:$GUNICORN_PORT" \
    --workers "$GUNICORN_WORKERS" \
    --timeout "$GUNICORN_TIMEOUT" \
    --log-level "$GUNICORN_LOG_LEVEL"
fi