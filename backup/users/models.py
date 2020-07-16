from django.db import models
from django.contrib.auth.models import AbstractUser

### ----- User models ------ ###
class User(AbstractUser):
    orcid_id = models.CharField(max_length=19)
    twitter = models.CharField(max_length=40)
    github = models.CharField(max_length=40)
    pass
