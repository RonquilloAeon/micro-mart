#!/bin/bash

# Wait for the database
while ! nc -z pool 6432; do
  sleep 1
done

python src/manage.py migrate

exec python src/manage.py runserver 0.0.0.0:8000
