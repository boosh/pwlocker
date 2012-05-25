from django.conf.urls.defaults import patterns, url

from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from apps.passwords.resources import PasswordResource

my_model_list = ListOrCreateModelView.as_view(resource=PasswordResource)
my_model_instance = InstanceModelView.as_view(resource=PasswordResource)

urlpatterns = patterns('',
    url(r'^passwords/$', my_model_list, name='model-resource-root'),
    url(r'^passwords/(?P<id>[0-9]+)/$', my_model_instance, name='model-resource-instance'),
)