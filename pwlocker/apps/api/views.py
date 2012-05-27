from djangorestframework.mixins import ModelMixin
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from apps.passwords.resources import PasswordResource

class RestrictToUserMixin(ModelMixin):
    """
    Mixin that restricts users to working with their own data
    """
    def get_queryset(self):
        """
        Only return objects created by the currently authenticated user.
        """
        return self.resource.model.objects.filter(created_by=self.user)

    def get_instance_data(self, model, content, **kwargs):
        """
        Set the created_by field to the currently authenticated user.
        """
        content['created_by'] = self.user
        return super(RestrictToUserMixin, self).get_instance_data(model, content, **kwargs)


class PasswordListView(RestrictToUserMixin, ListOrCreateModelView):
    """
    List view for Password objects.
    """
    resource = PasswordResource
    permissions = (IsAuthenticated, )


class PasswordInstanceView(RestrictToUserMixin, InstanceModelView):
    """
    View for individual Password instances
    """
    resource = PasswordResource
    permissions = (IsAuthenticated, )

