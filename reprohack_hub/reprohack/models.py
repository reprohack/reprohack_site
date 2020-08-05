from datetime import date, datetime

from taggit.managers import TaggableManager

from django.db import models
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

from config.settings.base import AUTH_USER_MODEL as User

RATING_MIN = 0
RATING_MAX = 10
# RATING_DEFUALT = 5


class Event(gismodels.Model):

    """An event to organise reproducing Paper results.

    Todo:
        * Should the host be another table?
        * Should the user be a "creator"?
        * Consider shifting date -> start_time, end_time
        * Should there be a ManyToManyField to Paper?
        * Consider UUIDs for URLs
        * Consider Venue Model separate to Event
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    host = models.CharField(max_length=200)
    title = models.CharField(_('Event Title'), max_length=200)
    # time
    date = models.DateField(default=date.today)
    time_start = models.TimeField(default=datetime.time(
        timezone.now().replace(minute=00, hour=10)))
    time_end = models.TimeField(default=datetime.time(
        timezone.now().replace(minute=00, hour=16)))
    # location
    location = models.CharField(max_length=200)  # Location name?
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=60)
    postcode = models.CharField(max_length=15)
    country = models.CharField(max_length=60)
    geom = Point()
    submission_date = models.DateTimeField(default=timezone.now)
    registration_url = models.URLField()

    def submit(self):
        self.submission_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.id])


class Author(models.Model):

    """Author of a paper.

    These are an extension of users to facilitate optional
    data if Paper authors are or become users.

    Todo:
        * Consider a different on_delete process (Author record stays
          irrespective of User account)
        * Through model
    """
    id = models.AutoField(primary_key=True)
    account = models.OneToOneField(User,
                                   on_delete=models.SET_NULL,
                                   null=True
                                   )
    # author_first_name = forms.EmailField(max_length=50)
    # author_last_name = forms.EmailField(max_length=50)
    # author_email = forms.EmailField(max_length=254)


# ---- Papers ---- #


class Paper(models.Model):

    """A paper to reproduce.

    Todo:
        * Consider UUIDs
        * Consider ForeignKey to Event (ManyToManyField)
        * Consider change user -> submitter
        * Consider clarifying submission_date (date paper is
          submitted to journal vs added to this database)
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(_("Paper Title"), max_length=200)
    event = models.ForeignKey(Event, null=True, blank=True,
                              on_delete=models.SET_NULL)
    available = models.BooleanField(_("Allow for review in any events"),
                                    default=True)
    citation_txt = models.TextField(max_length=300)
    doi = models.CharField(_("Eg: 10.1000/xyz123"), max_length=200,)
    description = models.TextField(max_length=400)
    why = models.TextField(max_length=400)
    focus = models.TextField(max_length=400)
    paper_url = models.URLField()
    code_url = models.URLField()
    data_url = models.URLField()
    extra_url = models.URLField()
    tools = TaggableManager()
    citation_bib = models.TextField(max_length=800)
    # submitter details
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    # authorship details
    authorship = models.BooleanField(default=True)
    # authors = models.ManyToManyField(Author,
    #                                  verbose_name="paper author(s)")
    # author_user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    contact = models.BooleanField(default=True)
    public = models.BooleanField(default=True)
    # feedback = models.BooleanField(default=True)
    submission_date = models.DateTimeField(default=timezone.now)
    archived = models.BooleanField(_("Removed from any reviews"), default=False,
                                   blank=True)

    def submit(self):
        self.submission_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('paper_detail', args=[self.id])


# class UnregisteredAuthor(models.Model):
#
#     """Model for data Authors not publicly registered.
#
#     Todo:
#         * Unsure of how this is meant to work
#         * Is this an extension of the user model? If so maybe inheritance is better
#         * If it's a base record so the user relationship is to an organiser, worth discussing
#         * from django.contrib.auth.models import AnonymousUser
#     """
#     user = models.OneToOneField(User,
#                                 on_delete=models.CASCADE,
#                                 primary_key=True)


# class ReportGroup(models.Model):
#     paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
#     members = models.ManyToManyField(
#         User,
#         through='Membership',
#         through_fields=('report_group', 'rep_author'),
#     )
#
#
# class Membership(models.Model):
#     report_group = models.ForeignKey(ReportGroup, on_delete=models.CASCADE)
#     rep_author = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):

    """A review of a Paper from either an individual or a group.

    There can be multiple reviews per paper, but if a paper
    is deleted from the database, by default related reviews
    will also be deleted.

    Todo:
        * Decide if there is a lead reviewer
        * Ask about reusability
        * Is contact email meant to be reviewer's (in their account?)
        * Consider removing the default rating to avoid bias
        * Ways of autocompleting paper selction
        * Generate an event option to connected to
    """

    FULLY_REPRODUCIBLE = 'y'
    PARTIALLY_REPRODUCIBLE = 'p'
    NOT_REPRODUCIBLE = 'n'
    REPRODUCIBILITY_OUTCOME_CHOICES = [
        (FULLY_REPRODUCIBLE, 'Fully Reproducible'),
        (PARTIALLY_REPRODUCIBLE, 'Partially Reproducible'),
        (NOT_REPRODUCIBLE, 'Not Reproducible')
    ]
    LINUX = 'linux'
    MACOS = 'macOS'
    WINDOWS = 'windows'
    OPERATING_SYSTEM_OPTIONS = [
        (LINUX, 'Linux/FreeBSD or other Open Source Operating system'),
        (MACOS, 'Apple Operating System'),
        (WINDOWS, 'Windows Operating System')
    ]

    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True)
    # Lead reviewer...?
    reviewers = models.ManyToManyField(User)
    reproducibility_description = models.TextField(_("Describe Reproducibility"),
                                                   blank=True, null=True)
    reproducibility_outcome = models.CharField(_("Categorise Reproducibility"),
                                               max_length=1,
                                               choices=REPRODUCIBILITY_OUTCOME_CHOICES,
                                               default=NOT_REPRODUCIBLE)
    reproducibility_rating = models.IntegerField(
        _("Overall Reproducibility Score"),
        # default=RATING_DEFUALT,  # Drop to avoid bias
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)]
    )
    operating_system = models.CharField(max_length=7,
                                        choices=OPERATING_SYSTEM_OPTIONS)
    operating_system_detail = models.CharField(max_length=100)
    software_installed = models.TextField()
    software_used = models.TextField()
    familiarity_with_method = models.TextField()
    challenges = models.TextField()
    advantages = models.TextField()
    comments_and_suggestions = models.TextField()
    documentation = models.TextField()
    documentation_rating = models.IntegerField(
        # default=RATING_DEFUALT,
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)]
    )
    documentation_cons = models.TextField()
    documentation_pros = models.TextField()
    method_familiarity = models.IntegerField(
        # default=RATING_DEFUALT,
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)]
    )
    method_reusability = models.IntegerField(  # Reusability?
        # default=RATING_DEFUALT,
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)]
    )
    data_permissive_license = models.BooleanField()
    code_permissive_license = models.BooleanField()
    reusability_suggestions = models.TextField()
    general_comments = models.TextField()
    # contact email should be included in user accounts,
