"""
The file provides default secret parameters used as a reference for creating your
own secret.py or in testing.

Make sure to create your own secret.py (in the same folder) with appropriate values for when deploying
the website!
"""
SECRET_KEY = "2r4-$a^!rs=^glu=a8m=e5a$5*wg2uxjjob!diff-z*wzdx+4y"
MYSQL_USERNAME = ""
MYSQL_PASSWORD = ""


"""
# Email Configuration - Specify e-mail backend here
# https://docs.djangoproject.com/en/3.2/topics/email/
# django-gmailapi-backend (https://github.com/dolfim/django-gmailapi-backend) is used for sending
# emails though Google's API. See README.md for more details.
"""


"""
Send e-mail through Gmail using Google's API
"""
EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'
GMAIL_API_CLIENT_ID = 'google_assigned_id'
GMAIL_API_CLIENT_SECRET = 'google_assigned_secret'
GMAIL_API_REFRESH_TOKEN = 'google_assigned_token'

"""
Send e-mail through standard SMTP serer. See [https://github.com/dolfim/django-gmailapi-backend](https://github.com/dolfim/django-gmailapi-backend)
for full list of configuration parameters.

Uncomment below to enable settings
"""
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'myserver.com'
# EMAIL_PORT = 22
# EMAIL_HOST_USER = 'username'
# EMAIL_HOST_PASSWORD = 'password'
