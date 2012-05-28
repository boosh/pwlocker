import datetime
import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from lib.utils import HTMLStripper

"""
Forms and validation code for user registration.
"""

class UserRegistrationForm(forms.Form):
    """
    Form for registering a new user.

    Uses the email address as the user name and only requires the password
    to be entered once.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30,
            widget=forms.TextInput(),
            label=_("User name"),
            error_messages={'required': _(u'Please enter a user name.')})
    email = forms.EmailField(widget=forms.TextInput(),
        max_length=75,
        label=_("E-mail address"),
        error_messages={'required': _(u'Please enter your e-mail address.')})
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_("Password"),
        min_length=8,
        error_messages={'required': _(u'Please enter a password.'),
            'min_length': _(u'Please enter at least %(limit_value)s characters.')})
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_("Confirm Password"),
        min_length=8,
        error_messages={'required': _(u'Please confirm your password.'),
            'min_length': _(u'Please enter at least %(limit_value)s characters.')})

    def clean_username(self):
        """
        Validate that the supplied username address is unique for the
        site.
        """
        username = self.cleaned_data['username']
        if not re.match('^[a-zA-Z \-_0-9]+$', username):
            raise forms.ValidationError(_("Your username may only contain spaces plus: a-z, 0-9, commas and full stops."))

        if User.objects.filter(username__iexact=username):
            raise forms.ValidationError(_("An account with this username already exists. "))
        return username

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("An account with this email address already exists. "))
        return self.cleaned_data['email']

    def clean_password2(self):
        """
        Make sure password1 == password2
        """
        try:
            if self.cleaned_data['password1'] == self.cleaned_data['password2']:
                return self.cleaned_data['password2']
        except KeyError:
            pass

        raise forms.ValidationError(_("Your passwords didn't match. Please enter them again."))


def user_created(sender, user, request, **kwargs):
    """
    Save extra fields to the user object and profile
    """
    stripper = HTMLStripper()
    form = UserRegistrationForm(request.POST)

    # form has already been validated, so just need to strip
    # whitespace
    user.username = stripper.strip(form.data["username"])
    user.first_name = stripper.strip(form.data["first_name"])
    user.last_name = stripper.strip(form.data["last_name"])
    user.save()


from registration.signals import user_registered
user_registered.connect(user_created)
