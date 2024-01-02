#!/bin/bash

# Apply database migrations
poetry run python manage.py migrate

# Collect static files
poetry run python manage.py runserver
