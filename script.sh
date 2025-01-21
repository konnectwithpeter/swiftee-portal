#!/bin/bash
python manage.py migrate
python manage.py process_tasks &
gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 3 zaffar.wsgi:application