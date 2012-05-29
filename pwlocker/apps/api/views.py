from django.db.models import Q
from djangorestframework.mixins import ModelMixin, InstanceMixin, \
ReadModelMixin, DeleteModelMixin
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView

from apps.passwords.models import PasswordContact
from apps.passwords.resources import PasswordResource, PasswordContactResource
from apps.users.resources import UserResource


class RestrictPasswordToUserMixin(ModelMixin):
    """
    Mixin that restricts users to working with their own data
    """
    def get_queryset(self):
        """
        Only return objects created by the currently authenticated user.
        """
        return self.resource.model.objects.filter(Q(created_by=self.user) |
            Q(shares__to_user=self.user))

    def get_instance_data(self, model, content, **kwargs):
        """
        Set the created_by field to the currently authenticated user.
        """
        content['created_by'] = self.user
        return super(RestrictPasswordToUserMixin, self).get_instance_data(model, content, **kwargs)


class PasswordListView(RestrictPasswordToUserMixin, ListOrCreateModelView):
    """
    List view for Password objects.
    """
    resource = PasswordResource
    permissions = (IsAuthenticated, )


class PasswordInstanceView(RestrictPasswordToUserMixin, InstanceModelView):
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

    def get_queryset(self):
        """
        Only return objects where the from_user is the currently authenticated user.
        """
        return self.resource.model.objects.filter(from_user=self.user)

    def get_instance_data(self, model, content, **kwargs):
        """
        Set the from_user field to the currently authenticated user.
        """
        content['from_user'] = self.user
        return super(PasswordContactListView, self).get_instance_data(model, content, **kwargs)


class ReadOnlyInstanceModelView(InstanceMixin, ReadModelMixin, ModelView):
    """
    A view which provides default operations for read/delete against a model instance
    but that prevents updates.
    """
    _suffix = 'Instance'


class PasswordContactReadOrDeleteInstanceView(ReadOnlyInstanceModelView):
    """
    View for individual PasswordContact instances
    """
    resource = PasswordContactResource
    permissions = (IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        """
        Deletes shares from Passwords when a PasswordContact is deleted
        """
        model = self.resource.model
        query_kwargs = self.get_query_kwargs(request, *args, **kwargs)

        try:
            instance = self.get_instance(**query_kwargs)
        except model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND, None, {})

        # remove any shares from any passwords shared with this contact
        password_contacts = PasswordContact.objects.filter(from_user=self.user,
            to_user=instance.to_user)

        for password_contact in password_contacts:
            password_contact.delete()

        instance.delete()
        return


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