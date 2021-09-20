#!/bin/bash
export DJANGO_SETTINGS_MODULE="config.settings.pythonanywhere"

# Activate the virtual environment
source .virtualenv/bin/activate

# Pull the update from git
git pull

# Make sure virtualenv is updated with an changes to dependencies
pip install -r requirements/pythonanywhere.txt

# Make sure the database is updated
./manage.py migrate

# Collect the static assets into /staticfiles folder
./manage.py collectstatic --noinput

# Compress templates
./manage.py compress

# Force pythonanywhere to reload app
touch /var/www/reprohacks_eu_pythonanywhere_com_wsgi.py
