from .production import *

DEBUG = False

ALLOWED_HOSTS += ["reprohacks.eu.pythonanywhere.com", "reprohack.org"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "reprohacks$reprohack_db",
        "HOST": "reprohacks.mysql.eu.pythonanywhere-services.com",
        "USER": MYSQL_USERNAME,
        "PASSWORD": MYSQL_PASSWORD,
        "PORT": "3306",
    }
}
