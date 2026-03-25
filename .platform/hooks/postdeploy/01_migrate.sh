#!/bin/bash
source /var/app/venv/*/bin/activate
cd /var/app/current
mkdir -p /var/app/current/staticfiles
python manage.py migrate --noinput || true
python manage.py collectstatic --noinput