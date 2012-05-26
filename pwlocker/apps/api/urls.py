from django.conf.urls.defaults import patterns, url

from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from apps.passwords.resources import PasswordResource

password_list = ListOrCreateModelView.as_view(resource=PasswordResource)
password_instance = InstanceModelView.as_view(resource=PasswordResource)

urlpatterns = patterns('',
    url(r'^passwords/$', password_list, name='passwords_api_root'),
    url(r'^passwords/(?P<id>[0-9]+)$', password_instance, name='passwords_api_instance'),
)