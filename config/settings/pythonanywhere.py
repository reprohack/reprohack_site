from .production import *

DEBUG = False

ALLOWED_HOSTS += ["reprohacks.eu.pythonanywhere.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "reprohack",
        'HOST': 'reprohacks.mysql.eu.pythonanywhere-services.com',
        'USER': MYSQL_USERNAME,
        'PASSWORD': MYSQL_PASSWORD,
    }
}
