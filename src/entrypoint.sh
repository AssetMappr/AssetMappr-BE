#!/bin/sh

# Migrate database
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Run gunicorn web server
gunicorn asset_mappr.wsgi:application --bind 0.0.0.0:8000