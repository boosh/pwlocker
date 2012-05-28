from djangorestframework.resources import ModelResource

from django.contrib.auth.models import User


class UserResource(ModelResource):
    """
    Lets users search for other users by username.
    """
    model = User
    fields = ('id', 'first_name', 'last_name', 'username', 'url')
    ignore_fields = ('id',)

    def validate_request(self, data, files=None):
        """
        Backbone.js will submit all fields in the model back to us, but
        some fields are set as uneditable in our Django model. So we need
        to remove those extra fields before performing validation.
        """
        for key in self.ignore_fields:
            if key in data:
                del data[key]

        return super(UserResource, self).validate_request(data, files)
