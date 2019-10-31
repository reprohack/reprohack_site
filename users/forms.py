from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column, HTML, Field
from crispy_forms.bootstrap import PrependedText
from users.models import User
from timezone_field import TimeZoneField

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ['timezone']

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        #self.email = self.cleaned_data['email']
        self.fields['orcid_id'].widget.attrs['placeholder'] = "0000-0000-0000-0000"
        self.fields['email'].required = True
        self.fields['twitter'].required = False
        self.fields['github'].required = False
        self.fields['orcid_id'].required = False
        self.helper = FormHelper(self) 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update'))
        self.helper.layout = Layout(
            HTML('<br><h4> Account details </h4>'),
            Row(Column('username', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-8 mb-0'), 
                css_class='form-row'),
            Row(Column('password', css_class='form-group col-md-6 mb-0'),
               # Column('password2', css_class='form-group col-md-6 mb-0')
                ),
            HTML('<br><h4> User details </h4>'),    
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'), 
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(
                Column('orcid_id', css_class='form-group col-md-10 mb-0'), 
                css_class='form-row'),
            Row(
                Column(PrependedText('twitter', '@', placeholder="twitter username"), css_class='form-group col-md-6 mb-0'),
                Column(PrependedText('github', '@', placeholder="github username"), css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            )
        )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ['timezone']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        #self.email = self.cleaned_data['email']
        self.fields['orcid_id'].widget.attrs['placeholder'] = "0000-0000-0000-0000"
        self.fields['email'].required = True
        self.fields['twitter'].required = False
        self.fields['github'].required = False
        self.fields['orcid_id'].required = False
        self.helper = FormHelper(self) 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.layout = Layout(
            HTML('<br><h4> Account details </h4>'),
            Row(Column('username', css_class='form-group col-md-4 mb-0'), 
                Column('email', css_class='form-group col-md-8 mb-0'), 
                css_class='form-row'),
            Row(Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0')),
            HTML('<br><h4> User details </h4>'),    
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'), 
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(
                Column('orcid_id', css_class='form-group col-md-10 mb-0'), 
                css_class='form-row'),
            Row(
                Column(PrependedText('twitter', '@', placeholder="twitter username"), css_class='form-group col-md-6 mb-0'),
                Column(PrependedText('github', '@', placeholder="github username"), css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            )
        )