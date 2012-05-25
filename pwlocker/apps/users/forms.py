from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

"""
Forms and validation code for user registration.
"""

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}


class UserRegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Uses the email address as the user name and only requires the password
    to be entered once.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    """
    first_name = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs=attrs_dict),
            label=_("First name"),
            error_messages={'required': _(u'Please enter your first name.')})
    last_name = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs=attrs_dict),
            label=_("Last name"),
            error_messages={'required': _(u'Please enter your last name.')})
    email = forms.EmailField(widget=forms.TextInput(),
        max_length=75,
        label=_("E-mail address"),
        error_messages={'required': _(u'Please enter your e-mail address.')})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"),
                                error_messages={'required': _(u'Please enter a password.')})

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            reset_password = reverse('django.contrib.auth.views.password_reset')
            raise forms.ValidationError(_("This email address is already in use. "
                '<a href="%s">Forgotten your password?</a>') % (reset_password))
        return self.cleaned_data['email']


class EmailAuthenticationForm(AuthenticationForm):
    """
    Changes the label on the uesrname field of the default authentication form
    to 'email'
    """
    username = forms.CharField(label=_("E-mail"), max_length=75)

    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
        reset_password = reverse('django.contrib.auth.views.password_reset')
        self.fields['password'].help_text=_('<a href="%s">Forgotten your password?</a>'
            % reset_password)

#from models import UserProfile

#class UserProfileForm(ModelForm):
#    """
#    Form to let users edit settings for the site.
#    """
#
#    class Meta:
#        model = UserProfile



def user_created(sender, user, request, **kwargs):
    """
    Save extra fields to the user object and profile
    """
    form = UserRegistrationForm(request.POST)

    # form has already been validated, so just need to strip
    # whitespace
    user.first_name = form.data["first_name"].strip()
    user.last_name = form.data["last_name"].strip()
    user.username = form.data["email"].strip()
    user.save()

from registration.signals import user_registered
user_registered.connect(user_created)
