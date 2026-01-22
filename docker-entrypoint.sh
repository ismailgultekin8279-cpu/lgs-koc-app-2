#!/bin/bash
set -e

# Move frontend build to a place Django can find or directly to staticfiles
# Assuming we configured Django to look into 'frontend_build' via STATICFILES_DIRS
# OR we just copy them to staticfiles directly here.

echo "Collecting static files..."
# We need to ensure STATICFILES_DIRS includes the build or we copy it.
# Let's assume we copy /app/frontend_build assets to /app/staticfiles manually
# effectively simulating collectstatic for the frontend part.
mkdir -p /app/staticfiles
cp -r /app/frontend_build/* /app/staticfiles/

# Run django collectstatic for admin and other static files
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn backend_project.wsgi:application --bind 0.0.0.0:8000
