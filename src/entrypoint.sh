#!/bin/sh

# Activate virtual environment 
. venv/bin/activate

# Make migrations
python manage.py makemigrations assets user --no-input

# Migrate database
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Run gunicorn web server
gunicorn asset_mappr.wsgi:application --bind 0.0.0.0:8000