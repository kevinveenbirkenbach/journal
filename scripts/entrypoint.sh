#!/bin/bash

pip install --no-cache-dir -r /app/requirements.txt

# Migrate database
bash /app/scripts/migrate.sh

if [ $? -ne 0 ]; then
    echo "Migration failed!"
    exit 1
fi

if [ "$DEBUG" == "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    # Specify the command to run on container start
    gunicorn "journal_project.wsgi:application" --bind "0.0.0.0:8000"
fi
