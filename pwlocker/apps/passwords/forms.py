from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _

from models import Password, PasswordContact

class PasswordForm(ModelForm):
    class Meta:
        model = Password
        widgets = {
            'shares': widgets.CheckboxSelectMultiple
        }

    def __init__(self, user, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        remove_message = unicode(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))

        for field in self.fields:
            if remove_message in self.fields[field].help_text:
                self.fields[field].help_text = self.fields[field].help_text.replace(remove_message, '').strip()

        # restrict the choice of users to share passwords with to a
        # user's PasswordContacts
        self.fields['shares'] = ModelMultipleChoiceField(
            queryset=PasswordContact.objects.filter(from_user=user) \
                .order_by('to_user__first_name'),
            widget=widgets.CheckboxSelectMultiple())