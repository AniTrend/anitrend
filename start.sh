#!/usr/bin/env bash

set -e

DEBUG_MODE=false

usage() {
 echo "Unrecognised option: -$OPTARG" >&2
 echo "Usage: $0 [OPTIONS]"
 echo "Options:"
 echo " -h    Display this help message"
 echo " -d    Run server in debug mode"
 echo " -w    Start work scheduler"
}

migrations() {
  echo "Checking and starting migrations"
  python manage.py makemigrations
  python manage.py migrate
}

cluster() {
  echo "Starting qcluster"
  python manage.py qcluster &
}

collect_static() {
    echo 'Collecting static files...'
    python manage.py collectstatic --no-input
}

start_dev_server() {
  python manage.py runserver "0.0.0.0:$PORT"
}

start_prod_server() {
  gunicorn "$APP_NAME.wsgi:application" \
    --bind "0.0.0.0:$GUNICORN_PORT" \
    --workers "$GUNICORN_WORKERS" \
    --timeout "$GUNICORN_TIMEOUT" \
    --log-level "$GUNICORN_LOG_LEVEL"
}

start_service() {
  migrations

  if $Q_CLUSTER; then
    cluster
  fi

  echo "Starting server"
  if $DEBUG_MODE; then
    collect_static
    start_dev_server
  else
    start_prod_server
  fi
}

while getopts ":wd:h" opt; do
  case ${opt} in
    w)
      Q_CLUSTER=true
      ;;
    d)
      DEBUG_MODE=true
      PORT="$OPTARG"
      ;;
    h)
      usage
      exit 0
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
    \?)
      usage
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

start_service
