from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.
class Password(models.Model):
    """
    Represents a password together with several other fields
    """
#    owner = models.ForeignKey(User, related_name='created_by',
#        editable=False)
    title = models.CharField(max_length=200)
    username = models.CharField(max_length=200,
        blank=True)
    password = models.CharField(max_length=200)
    # djangorestframework adds its own field called 'url' to the
    # representation of the object, so we need to use something else
    site_url = models.URLField(max_length=500,
        blank=True,
        verbose_name='Site URL')
    notes = models.TextField(
        max_length=500,
        blank=True,
        help_text='Any extra notes')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('password_show', args=[self.id])
