#!/usr/bin/env bash

echo "Starting migrations"
python manage.py migrate
echo "Starting qcluster"
python manage.py qcluster