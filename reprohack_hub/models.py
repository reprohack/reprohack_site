"""
ReproHack Venue, Event, Author, Paper and Review models.

Todo:
    * Check if default submission_date for Event and Paper is redundant.
"""

from datetime import datetime

from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

from markdownx.models import MarkdownxField

from timezone_field import TimeZoneField

from taggit.managers import TaggableManager

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.db.models import CharField


from django.db.models.signals import post_save
from django.dispatch import receiver

from reprohack_hub.utils import next_x_hour

RATING_MIN = 0
RATING_MAX = 10
RATING_DEFAULT = 5

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
class User(AbstractUser):
    """Default user for ReproHack Hub.

    Todo:
        * Consider Surname and Other (first, middle etc.) names
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    bio = models.TextField(max_length=500, blank=True)
    affiliation = models.CharField(max_length=70, blank=True)
    location = models.CharField(max_length=70, blank=True)
    twitter = models.CharField(max_length=15, blank=True)
    github = models.CharField(max_length=39, blank=True)
    orcid = models.CharField(max_length=17, blank=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("user_detail", kwargs={"username": self.username})



def default_event_start(hour: int = DEFAULT_EVENT_START_HOUR) -> datetime:
    """Return next default start time."""
    return next_x_hour(hour)


def default_event_end(hour: int = DEFAULT_EVENT_END_HOUR) -> datetime:
    """Return next default start time."""
    return next_x_hour(hour, default_event_start())


class Event(models.Model):

    """An event to organise reproducing Paper results.

    Todo:
        * Consider UUIDs for URLs
        * Consider Venue Model separate to Event
        * Auto-set to locale of user at point of login
    """

    # id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    host = models.CharField(max_length=200)
    title = models.CharField(_('Event Title'), max_length=200)
    # time
    # date = models.DateField(default=date.today)
    start_time = models.DateTimeField(default=default_event_start)
    end_time = models.DateTimeField(default=default_event_end)
    time_zone = TimeZoneField(default='Europe/London')
    # remote = models.BooleanField(default=False)

    # location
    # venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    description = MarkdownxField(_('Venue description (eg. entrance, '
                                   'parking etc.)'))
    # location = models.CharField(max_length=200)  # Location name?
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=60)
    postcode = models.CharField(max_length=15)
    country = CountryField()
    registration_url = models.URLField()
    event_coordinates = models.TextField(blank=True, null=True, )


    submission_date = models.DateTimeField(auto_now_add=True)
    # remote = models.BooleanField(default=False)

    # def submit(self):
    #     self.submission_date = get_time_zone.now()
    #     self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.id])

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def address(self):
        addr_items = [self.address1, self.address2, self.city, self.postcode, self.country.name]

        used_addr_items = []
        for addr_item in addr_items:
            if addr_item and isinstance(addr_item, str) and len(addr_item.strip()) > 0:
                used_addr_items.append(addr_item.strip())

        return ", ".join(used_addr_items)




    @property
    def lat(self):
        return self.decompress_lat_long(0)

    @property
    def long(self):
        return self.decompress_lat_long(1)

    def decompress_lat_long(self, decompressed_value_index):
        if self.event_coordinates:
            lat_long_split = self.event_coordinates.split(",")
            if len(lat_long_split) > 1:
                return lat_long_split[decompressed_value_index]

        return None

# ---- Papers ---- #


class Paper(models.Model):

    class ReviewAvailability(models.TextChoices):
        ALL = 'ALL', _('Allowed for reviews in any events')
        EVENT_ONLY = 'EVT_ONLY', _('Only allowed to review for associated event')
        ARCHIVE = 'ARCHIVE', _('Archive the paper, reviews are not allowed')

    """A paper to reproduce.

    Todo:
        * Consider UUIDs for url
        * Consider clarifying submission_date (date paper is
          submitted to journal vs added to this database)
        * Could test DOI with https://github.com/fabiobatalha/crossrefapi
        * Consider shifting contact boolean to AuthorsAndSubmitters
    """

    title = models.TextField(_("Paper Title"))
    authors = models.TextField(_("Authors"))
    event = models.ForeignKey(Event, null=True, blank=True,
                              on_delete=models.SET_NULL)

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

    submission_date = models.DateTimeField(auto_now_add=True)
    review_availability = models.CharField(_("Paper review permission"),
                                           choices=ReviewAvailability.choices,
                                           default=ReviewAvailability.ALL,
                                           max_length=20)
    public_reviews = models.BooleanField(_("Make reviews public"), default=True)
    email_review = models.BooleanField(_("Send me an email when a review is received"), default=True)
    submitter = models.ForeignKey(get_user_model(), default=None, null=True, blank=True, on_delete=models.SET_NULL)

    def get_reviews_viewable_by_user(self, user):
        reviews_list = []
        for review in self.review_set.all():
            if review.is_viewable_by_user(user):
                reviews_list.append(review)

        return reviews_list


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
        * Change choice widget for ratings (like google form)
    """

    class ReproducibilityOutcomes(models.TextChoices):
        FULLY_REPRODUCIBLE = 'y', _('Fully Reproducible'),
        PARTIALLY_REPRODUCIBLE = 'p', _('Partially Reproducible'),
        NOT_REPRODUCIBLE = 'n', _('Not Reproducible')


    class OperatingSystems(models.TextChoices):
        LINUX = 'linux', _('Linux/FreeBSD or other Open Source Operating system')
        MACOS = 'macOS', _('Apple Operating System')
        WINDOWS = 'windows', _('Windows Operating System')



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
                                               choices=ReproducibilityOutcomes.choices,
                                               default=ReproducibilityOutcomes.NOT_REPRODUCIBLE)
    reproducibility_rating = models.IntegerField(
        _("How much of the paper did you manage to reproduce?"),
        default=RATING_DEFAULT,
        validators=[MinValueValidator(RATING_MIN),
                    MaxValueValidator(RATING_MAX)],
        choices=RATING_CHOICES,
    )
    reproducibility_description = models.TextField(_("Briefly describe the "
                                                     "procedure followed/tools "
                                                     "used to reproduce it."),)
    familiarity_with_method = models.TextField(_("Briefly describe your "
                                                 "familiarity with the "
                                                 "procedure/tools used by "
                                                 "the paper."))
    operating_system = models.CharField(_("Which type of operating system were you "
                                          "working in?"), max_length=7,
                                        choices=OperatingSystems.choices)
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
        default=RATING_DEFAULT,
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
        default=RATING_DEFAULT,
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
        default=RATING_DEFAULT,
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

    public_review = models.BooleanField(_("Allow this review to be made public"), default=True)


    def __str__(self):
        """Default display of review.

        Todo:
            * Consider adding reviewer list or 'et al.'.
        """
        return (f"Review of '{self.paper}' by " +
                str(self.get_lead_reviewers().first()))

    def get_lead_reviewers(self):
        res = self.reviewers.filter(paperreviewer__lead_reviewer=True)
        return res

    def get_normal_reviewers(self):
        return self.reviewers.filter(paperreviewer__lead_reviewer=False)

    def get_absolute_url(self):
        return reverse('review_detail', args=[self.id])

    def is_viewable_by_user(self, user):
        # If public then viewable by everyone
        if self.public_review:
            return True

        # Otherwise you'd have to be logged in
        if isinstance(user, AnonymousUser):
            return False

        # Viewable by all reviweres
        for reviewer in self.reviewers.all():
            if reviewer.pk == user.pk:
                return True

        # And by the paper submitter
        if self.paper.submitter.pk == user.pk:
            return True

        return False

    def is_editable_by_user(self, user):


        # Have to be logged in
        if isinstance(user, AnonymousUser):
            return False

        # Viewable by all reviweres
        for reviewer in self.reviewers.all():
            if reviewer.pk == user.pk:
                return True

        return False



class PaperReviewer(models.Model):
    """
    A group of paper reviewers.
    """

    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lead_reviewer = models.BooleanField(default=True)



