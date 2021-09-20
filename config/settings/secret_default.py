"""
The file provides default secret parameters used as a reference for creating your
own secret.py or in testing.

Make sure to create your own secret.py (in the same folder) with appropriate values for when deploying
the website!
"""
SECRET_KEY = "2r4-$a^!rs=^glu=a8m=e5a$5*wg2uxjjob!diff-z*wzdx+4y"

"""
Set these if mysql is used as a database backend
"""
MYSQL_USERNAME = ""
MYSQL_PASSWORD = ""


"""
Set these if you're sending e-mail through Gmail using Google's API
"""
SECRET_GMAIL_API_CLIENT_ID = 'google_assigned_id'
SECRET_GMAIL_API_CLIENT_SECRET = 'google_assigned_secret'
SECRET_GMAIL_API_REFRESH_TOKEN = 'google_assigned_token'

"""
Set these if you're sending e-mail through SMTP
"""
SECRET_EMAIL_HOST_USER = 'username'
SECRET_EMAIL_HOST_PASSWORD = 'password'
