from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from apps.passwords.resources import PasswordResource

class PasswordListView(ListOrCreateModelView):
    """
    List view for Password objects.
    """
    resource = PasswordResource
    permissions = (IsAuthenticated, )

    def get_queryset(self):
        """
        Only return objects created by the currently authenticated user.
        """
        return self.resource.model.objects.filter(created_by=self.user)

    def post(self, request, *args, **kwargs):
        """
        self.user is a property created by the AuthMixin. So we can simply
        update the submitted content dict to set the created_by field to the
        currently authenticated user.
        """
        self.CONTENT['created_by'] = self.user
        return super(PasswordListView, self).post(request, *args, **kwargs)


class PasswordInstanceView(InstanceModelView):
    """
    View for individual Password instances
    """
    resource = PasswordResource
    permissions = (IsAuthenticated, )