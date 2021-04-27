from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML, Field
from crispy_forms.bootstrap import InlineRadios
# from leaflet.forms.widgets import LeafletWidget

from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from leaflet.forms.widgets import LeafletWidget

from .models import Event, Paper, Review

# -------- Event -------- #
LEAFLET_WIDGET_ATTRS = {
    'DEFAULT_CENTER': (6.0, 45.0),
    'DEFAULT_ZOOM': 5,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
}


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['submission_date', 'creator', ]
        widgets = {'geom': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS)}

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator')
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit event'))
        self.helper.layout = Layout(
            'title',
            'host',
            Row(
                Column('start_time', css_class='form-group col-md-4 mb-0'),
                Column('end_time', css_class='form-group col-md-4 mb-0'),
                Column('time_zone', css_class='form-group col-md-4 mb-0'),
                css_class='form-row',
            ),
            # 'venue',
            'description',
            'address1',
            'address2',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('postcode', css_class='form-group col-md-3 mb-0'),
                Column('country', css_class='form-group col-md-3 mb-0'),
            ),
            'registration_url',
            'geom',
        )


# -------- Paper -------- #
class PaperForm(ModelForm):
    class Meta:
        model = Paper
        exclude = ['submission_date', 'creator', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PaperForm, self).__init__(*args, **kwargs)
        # self.email = self.cleaned_data['email']

        # self.fields['authorship'].label = "I am the corresponding author"
        # self.fields['contact'].label = "I can be contacted by participants"

        # self.fields['feedback'].label = "I wish to received feedback on reproductions"
        self.fields['public'].label = "I wish to receive feedback on reproductions"
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit paper'))
        self.helper.layout = Layout(
            HTML('<h2>Paper details<h2>'),
            'title',
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
            Field('tools', label="Useful Software Skills"),
            HTML('<h3>Submitter contact details<h3>'),
            Row(
                Column(css_class='form-group col-md-4 mb-0'),
                css_class='form-row',
            ),
            Fieldset("Authorship details",
                     # Row(
                     #     Column('authorship', label="I am corresponding author",
                     #            css_class='form-group col-md-6 mb-0'),
                     #     Column('author_first_name',
                     #            css_class='form-group col-md-3 mb-0'),
                     #     Column('author_last_name',
                     #            css_class='form-group col-md-3 mb-0'),
                     #     Column('author_email',
                     #            css_class='form-group col-md-6 mb-0'),
                     #     css_class='form-row',
                     # ),
                     Row(
                         Column('public', label="Feedback can be published",
                                css_class='form-group col-md-6 mb-0'),
                         css_class='form-row',
                     ),
                     ),
        )

    # def clean(self):
    #     authorship = self.cleaned_data.get('authorship')

    #     if authorship:
    #         self.cleaned_data['author_user'] = self.user
    #     else:
    #         self.cleaned_data['author_user'] = ""
    #         self.fields_required(['author_first_name'])
    #         self.fields_required(['author_last_name'])
    #         self.fields_required(['author_email'])
    #     return self.cleaned_data

    # def fields_required(self, fields):
    #     for field in fields:
    #         if not self.cleaned_data.get(field, ''):
    #             msg = forms.ValidationError("This field is required.")
    #             self.add_error(field, msg)


class ReviewForm(ModelForm):

    """A form to review papers.

    Todo:
        * Test the query of available papers with respect to event.
    """

    class Meta:
        model = Review
        exclude = ['reviewers', ]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['paper'].queryset = Paper.objects.filter(available=True)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit review'))
        self.helper.layout = Layout(
            # HTML('<h2>ReproHack Author Feedback Form</h2>'),
            'event',
            'paper',
            HTML(f"<h3>{_('Reproducibility')}</h3>"),
            'reproducibility_outcome',
            InlineRadios('reproducibility_rating'),
            'reproducibility_description',
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
        )


# --------------- USER PROFILE ---------------------- #


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = get_user_model()
        exclude = ["password", "id_password"]
        fields = ['name', 'email', 'bio', 'affiliation', 'location', 'twitter', 'github', 'orcid']


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        fields = ('first_name', "last_name", 'username', 'email', 'password1', 'password2')
        model = get_user_model()

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign up'))
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-5 mb-0'),
                Column('last_name', css_class='form-group col-md-7 mb-0')
            ),
            'username',
            'email',
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0')
            )

        )
