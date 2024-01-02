#!/bin/bash
sleep 30
# Apply database migrations
poetry run python manage.py migrate

# Collect static files
poetry run python manage.py runserver 0.0.0.0:8000
