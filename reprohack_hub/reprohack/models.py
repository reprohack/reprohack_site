"""
ReproHack Venue, Event, Author, Paper and Review models.

Todo:
    * Check if default submission_date for Event and Paper is redundant.
"""

from datetime import datetime

from markdownx.models import MarkdownxField

from timezone_field import TimeZoneField

from taggit.managers import TaggableManager

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models

from config.settings.base import AUTH_USER_MODEL as User

from .utils import next_x_hour

RATING_MIN = 0
RATING_MAX = 10

DEFAULT_EVENT_START_HOUR = 10
DEFAULT_EVENT_END_HOUR = 16


# class Venue(models.Model):
#
#     """Venue with spatial coordinates.
#
#     To ensure this is likely to be user faced, users should only see Venues
#     related to Events they create.
#     """
#
#     # id = models.AutoField(primary_key=True)
#     # creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     detail = models.CharField(_('Eg: Room #'), max_length=300)
#     address1 = models.CharField(max_length=200)
#     address2 = models.CharField(max_length=200)
#     city = models.CharField(max_length=60)
#     postcode = models.CharField(max_length=15)
#     country = models.CharField(max_length=60)
#     geom = models.PointField(blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     # def get_absolute_url(self):
#     #     return reverse('venue_detail', args=[self.id])


def default_event_start(hour: datetime = DEFAULT_EVENT_START_HOUR) -> datetime:
    """Return next default start time."""
    return next_x_hour(hour)


def default_event_end(hour: datetime = DEFAULT_EVENT_END_HOUR) -> datetime:
    """Return next default start time."""
    return next_x_hour(hour, default_event_start())


class Event(models.Model):

    """An event to organise reproducing Paper results.

    Todo:
        * Consider UUIDs for URLs
        * Consider Venue Model separate to Event
    """

    # id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    host = models.CharField(max_length=200)
    title = models.CharField(_('Event Title'), max_length=200)
    # time
    # date = models.DateField(default=date.today)
    start_time = models.DateTimeField(default=default_event_start)
    end_time = models.DateTimeField(default=default_event_end)
    time_zone = TimeZoneField(default='Europe/Berlin')
    # remote = models.BooleanField(default=False)

    # location
    # venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    # location = models.CharField(max_length=200)  # Location name?
    venue_description = MarkdownxField(_('Venue description (eg. entrance, '
                                         'parking etc.)'))
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=60)
    postcode = models.CharField(max_length=15)
    country = models.CharField(max_length=60)
    geom = models.PointField(blank=True, null=True)
    registration_url = models.URLField()

    submission_date = models.DateTimeField(auto_now_add=True)
    # remote = models.BooleanField(default=False)

    # def submit(self):
    #     self.submission_date = get_time_zone.now()
    #     self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.id])


# ---- Papers ---- #


class Paper(models.Model):

    """A paper to reproduce.

    Todo:
        * Consider UUIDs for url
        * Consider clarifying submission_date (date paper is
          submitted to journal vs added to this database)
        * Could test DOI with https://github.com/fabiobatalha/crossrefapi
        * Consider shifting contact boolean to AuthorsAndSubmitters
    """

    # id = models.AutoField(primary_key=True)
    title = models.CharField(_("Paper Title"), max_length=200)
    # events = models.ManyToManyField(Event, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True,
                              on_delete=models.SET_NULL)
    available = models.BooleanField(_("Allow for review in any events"),
                                    default=True)
    citation_txt = models.TextField(max_length=300)
    doi = models.CharField(_("DOI (eg. 10.1000/xyz123)"), max_length=200,)
    description = models.TextField(max_length=400)
    why = models.TextField(max_length=400)
    focus = models.TextField(max_length=400)
    paper_url = models.URLField()
    code_url = models.URLField()
    data_url = models.URLField()
    extra_url = models.URLField()
    tools = TaggableManager()
    citation_bib = models.TextField()
    # submitter details
    # submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    # authorship details
    authors_and_submitters = models.ManyToManyField(User,
                                                    through="AuthorsAndSubmitters",
                                                    through_fields=('paper', 'user'),)
    # authorship = models.BooleanField(default=True)
    #
    # authors = models.ManyToManyField(Author,
    #                                  verbose_name="paper author(s)")
    # author_user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    public = models.BooleanField(default=True)
    # feedback = models.BooleanField(default=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(_("Removed from any reviews"), default=False,
                                   blank=True)

    # def submit(self):
    #     self.submission_date = get_time_zone.now()
    #     self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('paper_detail', args=[self.id])


class AuthorsAndSubmitters(models.Model):

    """A group of authors and/or submitters of papers for review.

    Todo:
        * Consider other data (academic affiliation/status etc.) to add.
        * Potentially combine info here with Users for summary of authorship.
    """

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    contact = models.BooleanField(default=True)
    author = models.BooleanField(default=True)
    submitted = models.BooleanField(default=True)

    def clean(self):
        if not self.author and not self.submitter:
            raise ValidationError(_('Users must be either an author or '
                                    'submitter or both.'))

    # def __str__(self):
    #     return f"{self.user} {self.paper}"


class Review(models.Model):

    """A review of a Paper from either an individual or a group.

    There can be multiple reviews per paper, but if a paper
    is deleted from the database, by default related reviews
    will also be deleted.

    Based on this example:

    https://docs.google.com/forms/d/e/1FAIpQLSesByo93VRId3xD7EgiQFDW9ep_14tkyuZUm_VCVxXeDexKGw/viewform

    Todo:
        * Discuss ways of autocompleting paper selction (only future, flag on
          events, permission, etc.)
        * Consider Team issue URL
        * Consider additional descriptive list of reviewers without accounts
        * Add custom descriptions for rating max and min
        * Consider markdownx for descriptions
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
    RATING_CHOICES = [(x, x) for x in range(RATING_MIN, RATING_MAX + 1)]

    # id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event,
                              on_delete=models.SET_NULL,
                              null=True, blank=True)
    # Lead reviewer...?
    reviewers = models.ManyToManyField(User,
                                       through="PaperReviewer",
                                       through_fields=('review', 'user'),)
    #
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True)
    reproducibility_outcome = models.CharField(_("Did you manage to reproduce it?"),
                                               max_length=1,
                                               choices=REPRODUCIBILITY_OUTCOME_CHOICES,
                                               default=NOT_REPRODUCIBLE)
    reproducibility_rating = models.IntegerField(
        _("On a scale of 1 to 10, how much of the paper did you manage to "
          "reproduce?"),
        # default=RATING_DEFAULT,  # Drop to avoid bias
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)],
        choices=RATING_CHOICES,
    )
    reproducibility_description = models.TextField(_("Briefly describe the "
                                                     "procedure followed/tools"
                                                     "used to reproduce it."),)
    familiarity_with_method = models.TextField(_("Briefly describe your "
                                                 "familiarity with the "
                                                 "procedure/tools used by "
                                                 "the paper."))
    operating_system = models.CharField(_("Which type of operating system were you "
                                          "working in?"), max_length=7,
                                        choices=OPERATING_SYSTEM_OPTIONS)
    operating_system_detail = models.CharField(_("What operating system were you "
                                                 "using (eg. Ubuntu 14.04.6 LTS, "
                                                 "macOS 10.15 or Windows 10 Pro)?"),
                                               max_length=100)
    software_installed = models.TextField(_("What additional software did you need "
                                          "to install?"))
    software_used = models.TextField(_("What software did you use?"))
    challenges = models.TextField(_("What were the main challenges you ran "
                                    "into (if any)?"))
    advantages = models.TextField(_("What were the positive features of "
                                    "this approach?"))
    comments_and_suggestions = models.TextField(_("Any other comments/suggestions "
                                                  "on the reproducibility approach?"))
    documentation_rating = models.IntegerField(
        _("How well was the material documented?"),
        # default=RATING_DEFUALT,
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)],
        choices=RATING_CHOICES,
    )
    documentation_cons = models.TextField(_("How could the documentation "
                                            "be improved?"))
    documentation_pros = models.TextField(_("What do you like about the "
                                            "documentation?"))
    method_familiarity_rating = models.IntegerField(
        _("After attempting to reproduce, how familiar do you feel with "
          "the code and methods used in the paper?"),
        # default=RATING_DEFUALT,
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)],
        choices=RATING_CHOICES,
    )
    transparency_suggestions = models.TextField(
        _("Any suggestions on how the analysis could be made more "
          "transparent?")
    )
    method_reusability_rating = models.IntegerField(  # Reusability?
        _("Rate the project on reusability of the material."),
        # default=RATING_DEFUALT,
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)],
        choices=RATING_CHOICES,
    )
    # ("Are materials clearly "
    #  "covered by a " "permissive enough " "license to build " "on?")
    data_permissive_license = models.BooleanField(_("Permissive license "
                                                    "for DATA included"))
    code_permissive_license = models.BooleanField(_("Permissive license "
                                                    "for CODE included"))
    reusability_suggestions = models.TextField(_("Any suggestions on how "
                                                 "the project could be "
                                                 "more reusable?"))
    general_comments = models.TextField(_("Any final comments:"))
    submission_date = models.DateTimeField(auto_now_add=True)
    # contact email should be included in user accounts,

    def __str__(self):
        """Default display of review.

        Todo:
            * Consider adding reviewer list or 'et al.'.
        """
        return (f"Review of '{self.paper}' by " +
                str(self.get_lead_reviewers().first()))

    def get_lead_reviewers(self):
        return self.reviewers.filter(paperreviewer__lead_reviewer=True)

    def get_absolute_url(self):
        return reverse('review_detail', args=[self.id])


class PaperReviewer(models.Model):

    """A group of paper reviewers."""

    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lead_reviewer = models.BooleanField(default=True)
