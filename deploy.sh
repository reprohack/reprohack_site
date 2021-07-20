#!/bin/bash

# Activate the virtual environment
source .virtualenv/bin/activate

# Pull the update from git
git pull

# Make sure the databae is updated
./manage.py migrate

# Collect the static assets into /staticfiles folder
./manage.py collectstatic

# Force pythonanywhere to reload app
touch /var/www/reprohacks_eu_pythonanywhere_com_wsgi.py
