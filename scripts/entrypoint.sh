# Migrate database
bash migrate.sh

# Specify the command to run on container start
gunicorn "journal_project.wsgi:application" --bind "0.0.0.0:8000"