from djangorestframework.resources import ModelResource
from django.core.urlresolvers import reverse
from models import Password


class PasswordResource(ModelResource):
    model = Password
    ordering = ('-created_at',)

    def url(self, instance):
        return reverse('model-resource-instance',
                       kwargs={'id': instance.id})