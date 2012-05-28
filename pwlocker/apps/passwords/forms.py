from django.forms import ModelForm
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from models import Password

class PasswordForm(ModelForm):
    class Meta:
        model = Password
        widgets = {
            'shares': widgets.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        remove_message = unicode(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))

        for field in self.fields:
            if remove_message in self.fields[field].help_text:
                self.fields[field].help_text = self.fields[field].help_text.replace(remove_message, '').strip()