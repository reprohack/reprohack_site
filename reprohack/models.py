from django.conf import settings
from django.db import models
from django import forms
from django.utils import timezone
from datetime import date, datetime
from django.forms.widgets import TimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from djgeojson.fields import PointField
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

class Event(gismodels.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default="Event title")
    # time
    date = models.DateField(default=date.today)
    time_start = models.TimeField(default=datetime.time(timezone.now().replace(minute=00, hour=10)))
    time_end = models.TimeField(default=datetime.time(timezone.now().replace(minute=00, hour=16)))
    # location
    location = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=400, default='')
    city = models.CharField(max_length=60, default='')
    postcode = models.CharField(max_length=15, default='')
    geom = PointField(blank=True)
    submission_date = models.DateTimeField(default=timezone.now)
    registration_url = models.URLField()

    def submit(self):
        self.submission_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.id])
 
 # ---- Papers ---- #

class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, default="Event title")
    citation_txt = models.TextField(max_length=300)
    doi = models.CharField(max_length=200, default="10.1000/xyz123")
    description = models.TextField(max_length=400)
    why = models.TextField(max_length=400)
    focus = models.TextField(max_length=400)
    paper_url = models.URLField()
    code_url = models.URLField()
    data_url = models.URLField()
    extra_url = models.URLField()
    tools = TaggableManager()
    citation_bib = models.CharField(max_length=800)
    # submitter details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    twitter = models.CharField(max_length=40)
    github = models.CharField(max_length=40)
    # authorship details
    authorship = models.BooleanField(default=True)
    author_first_name = forms.EmailField(max_length=50)
    author_last_name = forms.EmailField(max_length=50)
    author_email = forms.EmailField(max_length=254)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    contact = models.BooleanField(default=True)
    public = models.BooleanField(default=True)
    #feedback = models.BooleanField(default=True)
    submission_date = models.DateTimeField(default=timezone.now)

    def submit(self):
        self.submission_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('paper_detail', args=[self.id])

class UnregisteredAuthor(models.Model)

class ReportGroup(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        User,
        through='Membership',
        through_fields=('report_group', 'user'),
    )

class Membership(models.Model):
    report_group = models.ForeignKey(ReportGroup, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE)
