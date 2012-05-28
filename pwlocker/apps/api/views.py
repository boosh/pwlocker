from django.db.models import Q
from djangorestframework.mixins import ModelMixin, InstanceMixin, \
ReadModelMixin, DeleteModelMixin
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView

from apps.passwords.resources import PasswordResource, PasswordContactResource
from apps.users.resources import UserResource

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


class PasswordContactListView(ListOrCreateModelView):
    """
    List view for PasswordContact objects.
    """
    resource = PasswordContactResource
    permissions = (IsAuthenticated, )

    def get_instance_data(self, model, content, **kwargs):
        """
        Set the created_by field to the currently authenticated user.
        """
        content['from_user'] = self.user
        return super(PasswordContactListView, self).get_instance_data(model, content, **kwargs)


class ReadOrDeleteInstanceModelView(InstanceMixin, ReadModelMixin, DeleteModelMixin, ModelView):
    """
    A view which provides default operations for read/delete against a model instance
    but that prevents updates.
    """
    _suffix = 'Instance'


class PasswordContactReadOrDeleteInstanceView(ReadOrDeleteInstanceModelView):
    """
    View for individual PasswordContact instances
    """
    resource = PasswordContactResource
    permissions = (IsAuthenticated, )


class UserView(InstanceMixin, ReadModelMixin, ModelView):
    """
    View for individual Users lets users find other users by username
    """
    resource = UserResource
    permissions = (IsAuthenticated, )

    def get_queryset(self):
        """
        Filter the current user from search results to prevent them sharing
        with themselves.
        """
        return self.resource.model.objects.filter(~Q(id=self.user.id))