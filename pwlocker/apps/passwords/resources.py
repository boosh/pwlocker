from djangorestframework.resources import ModelResource
from django.core.urlresolvers import reverse
from models import Password


class PasswordResource(ModelResource):
    model = Password
    # by default, django rest framework won't return the ID - backbone.js
    # needs it though, so don't exclude it
    exclude = None
    ordering = ('-created_at',)
    # django rest framework will overwrite our 'url' attribute with its own
    # that points to the resource, so we need to provide an alternative.
    include = ('resource_url',)

    def url(self, instance):
        """
        Return the instance URL. If we don't specify this, django rest
        framework will return a generated URL to the resource
        """
        return instance.url

    def resource_url(self, instance):
        """
        An alternative to the 'url' attribute django rest framework will
        add to the model.
        """
        return reverse('passwords_api_instance',
                       kwargs={'id': instance.id})