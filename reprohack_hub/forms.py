import logging
import json
from typing import Any, Optional, Dict, Union, Type, Sequence

from django.forms import Field as DFField, ModelForm, Widget, TextInput, RadioSelect, CharField, NumberInput
from django.forms.models import ModelChoiceField
from django.forms.widgets import Textarea
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML, Field, Div
from crispy_forms.bootstrap import InlineRadios, StrictButton, PrependedText, PrependedAppendedText
from datetimewidget.widgets import DateTimeWidget
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
# from leaflet.forms.widgets import LeafletWidget

from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError

from .models import Event, Paper, Review, PaperReviewer

logger = logging.getLogger(__name__)


# -------- Event -------- #
class MapInput(Widget):
    template_name = "event/map_input_widget.html"


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['submission_date', 'creator']
        widgets = {'event_coordinates': MapInput(),
                   'remote': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
                   'start_time': DateTimeWidget(attrs={'id': "start_time"},
                                                usel10n=True, bootstrap_version=3),
                   'end_time': DateTimeWidget(attrs={'id': "end_time"},
                                              usel10n=True, bootstrap_version=3),
                   }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(
            #StrictButton('Submit event', css_class="btn-success")
            Submit('submit', 'Submit event', css_class="boxed_btn")
        )
        self.helper.layout = Layout(
            'title',
            'host',
            Field('contact_email'),
            HTML("<small style='color: #7e7e7e;'>If no email supplied, the email associated with the account submitting the event will be used as contact.</small><br><br><br>"),
            'registration_url',
            'hackpad_url',
            Fieldset('Event Time/Date',
            Row(
                Column('start_time', css_class='form-group col-md-4 mb-0'),
                Column('end_time', css_class='form-group col-md-4 mb-0'),
                Column('time_zone', css_class='form-group col-md-4 mb-0'),
                css_class='form-row',
            )),
            Fieldset(
                'Event Location',
                'remote',
                'address1',
                'address2',
                Row(
                    Column('city', css_class='form-group col-md-6 mb-0'),
                    Column('postcode', css_class='form-group col-md-3 mb-0'),
                    Column('country', css_class='form-group col-md-3 mb-0'),
                ),
                'event_coordinates'),
            Fieldset('Event Description',
            'description'),
        )


# -------- Paper -------- #

class TagWidget(Widget):
    template_name = "paper/tag_input.html"

    def format_value(self, value):
        """
        Convert taggit's tag manger objects to plain comma separated text
        :param value:
        :return:
        """
        if value:
            return ",".join([tag.name for tag in value])

        return ""


class PaperForm(ModelForm):
    class Meta:
        model = Paper
        exclude = ['submission_date', 'creator', ]
        widgets = {
            'title': TextInput(),
            # 'review_availability': RadioSelect(),
            'authors': Textarea(attrs={'style': 'height:6em'}),
            'citation_txt': Textarea(attrs={'style': 'height:8rem'}),
            'citation_bib': Textarea(attrs={'style': 'height:12rem'}),
            'description': Textarea(attrs={'style': 'height:18rem'}),
            'why': Textarea(attrs={'style': 'height:18rem'}),
            'focus': Textarea(attrs={'style': 'height:12rem'}),
            'tags': TagWidget(),
            'archive': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
            'email_review': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
            'public_reviews': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
        }

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Submit paper', css_class="boxed_btn"))
        self.helper.layout = Layout(
            HTML('<h2>Paper details<h2>'),
            'event',
            'title',
            'authors',

            'citation_txt',
            'citation_bib',
            'doi',
            'description',
            'why',
            'focus',
            Fieldset("Links to Resources",
                     Row(
                         Column('paper_url', css_class='form-group col-md-6 mb-0'),
                         Column('data_url',  css_class='form-group col-md-6 mb-0'),
                         css_class='form-row',
                     ),
                     Row(
                         Column('code_url', css_class='form-group col-md-6 mb-0'),
                         Column('extra_url', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row',
                     ),
                     ),
            Field('tags', label="Useful Software Skills"),
            Fieldset("Review Availability",
                     "review_availability",
                     "archive"),
            Fieldset("Review Visibility",
                     Field("public_reviews"), type=""),
            Fieldset("Notifications",
                     "email_review")
        )


class MuWidget(Widget):

    template_name = "review/reviewers_select.html"

    def get_context(self, name: str, value: Any, attrs):
        context = super().get_context(name, value, attrs)
        context["user"] = self.user
        return context


class MuField(DFField):
    instance = None
    widget = MuWidget

    def clean(self, value):
        return value


class ReviewForm(ModelForm):

    """A form to review papers.

    Todo:
        * Test the query of available papers with respect to event.
    """

    reviewers = MuField()

    class Meta:
        model = Review
        exclude = ['reviewers']
        widgets = {'public_review': DjangoToggleSwitchWidget(
            round=True, klass="django-toggle-switch-success")}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["reviewers"].widget.user = self.user
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Submit Review', css_class="boxed_btn"))
        self.helper.layout = Layout(
            # HTML('<h2>ReproHack Author Feedback Form</h2>'),
            'reviewers',
            HTML('<p class="mt-3">To add a reviewer, type a username into the box above and <strong>press enter</strong>, then click on the <strong>Add a reviewer</strong> button<p>'),
            'paper',
            'event',
            HTML(f"<h3>{_('Reproducibility')}</h3>"),
            'reproducibility_outcome',
            InlineRadios('reproducibility_rating'),
            Field('reproducibility_description', css_class="md-large-box"),
            'familiarity_with_method',
            Fieldset(_("Operating System"),
                     Row(
                         Column('operating_system',
                                css_class='form-group col-md-4 mb-0'),
                         Column('operating_system_detail',
                                css_class='form-group col-md-8 mb-0')
            )),
            'software_installed',
            'software_used',
            'challenges',
            'advantages',
            'comments_and_suggestions',
            HTML('<h3>Documentation</h3>'),
            InlineRadios('documentation_rating'),
            'documentation_cons',
            'documentation_pros',
            InlineRadios('method_familiarity_rating'),
            'transparency_suggestions',
            HTML(f"<h3>{_('Reusability')}</h3>"),
            InlineRadios('method_reusability_rating'),
            Fieldset(_("Are materials clearly covered by a "
                       "permissive enough license to build on?"),
                     Row(
                         Column('data_permissive_license',
                                css_class='form-group col-md-6 mb-0'),
                         Column('code_permissive_license',
                                css_class='form-group col-md-6 mb-0'),
            )),
            'reusability_suggestions',
            'general_comments',
            Fieldset(_("Permissions"),
                     "public_review"
                     )
        )

    def clean(self) -> Dict[str, Any]:
        # user = self.user
        # raise ValidationError(f"Test returning error message", code='invalid')
        return super().clean()

    def save(self, commit: bool = ...) -> Any:
        save_result = super().save(commit)
        review = self.instance

        try:

            reviewers_data_str = self.cleaned_data["reviewers"]
            reviewers_data = json.loads(reviewers_data_str)

            review.reviewers.clear()
            for reviewer_obj in reviewers_data:
                user = get_user_model().objects.get(
                    username=reviewer_obj["username"])
                review.reviewers.add(user, through_defaults={
                                     "lead_reviewer": reviewer_obj["lead"]})
            review.save()

        except Exception as e:
            logger.exception("Trying to save an invalid reviewers list")

        return save_result


# --------------- USER PROFILE ---------------------- #


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = get_user_model()
        exclude = ["password", "id_password"]
        fields = ['full_name', 'preferred_name', 'email', 'bio', 'affiliation',
                  'location', 'twitter', 'github', 'orcid']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class="boxed_btn"))
        self.helper.layout = Layout(
            HTML("<h2> Account Details </h2>"),
            'email',
            Row(
                Column('full_name', css_class=''),

            ),
            Row(
                Column('preferred_name', css_class=''),

            ),
             Row(
                HTML("<div><label>Password</label><p><a href='/accounts/password/set'>Reset password using this form.</a></p></div>")
            ),
            HTML("<h2> Additional Profile Info </h2>"),
              Row(
                Column('bio', css_class='form-group col-md-6 mb-0'),
                Column('affiliation', 'location', css_class='form-group col-md-6 mb-0')
              ),
              Fieldset('Social',
              Row(
                Column(
                    PrependedAppendedText('twitter', '@', '<i class="fab fa-twitter"></i>',
                    placeholder="username"), css_class='form-group col-md-4 mb-0'
                ),
                Column(
                    PrependedAppendedText('github', '@', '<i class="fab fa-github"></i>',
                    placeholder="username"), css_class='form-group col-md-4 mb-0'
                    ),
                Column(
                    PrependedText('orcid', '<i class="fab fa-orcid"></i>',
                    placeholder="0000-0000-0000-0000",
                    title = 'ORCID ID'), css_class='form-group col-md-4 mb-0'
                    )
                )
              )
        )

class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        fields = ('full_name', 'preferred_name', 'username', 'email', 'password1',
                  'password2', 'affiliation', 'twitter', 'github', 'orcid',
                  'bio', 'location')
        model = get_user_model()


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit('submit', 'Sign up', css_class="boxed_btn"))
        self.helper.layout = Layout(
            HTML("<h2> Account Details </h2>"),
            'username',
            'email',
            Row(
                Column('full_name', css_class=''),

            ),
            Row(
                Column('preferred_name', css_class=''),

            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0')
            ),
            HTML("<h3> Additional Profile Info </h3>"),
              Row(
                Column('bio', css_class='form-group col-md-6 mb-0'),
                Column('affiliation', 'location', css_class='form-group col-md-6 mb-0')
              ),
              Fieldset('Social',
              Row(
                Column(
                    PrependedAppendedText('twitter', '@', '<i class="fab fa-twitter"></i>',
                    placeholder="username"), css_class='form-group col-md-4 mb-0'
                ),
                Column(
                    PrependedAppendedText('github', '@', '<i class="fab fa-github"></i>',
                    placeholder="username"), css_class='form-group col-md-4 mb-0'
                    ),
                Column(
                    PrependedText('orcid', '<i class="fab fa-orcid"></i>',
                    placeholder="0000-0000-0000-0000",
                    title = 'ORCID ID'), css_class='form-group col-md-4 mb-0'
                    )
                )
              )

        )
