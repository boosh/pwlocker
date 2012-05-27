from django.conf.urls.defaults import patterns, url

from views import PasswordListView, PasswordInstanceView

urlpatterns = patterns('',
    url(r'^passwords/$', PasswordListView.as_view(), name='passwords_api_root'),
    url(r'^passwords/(?P<id>[0-9]+)$', PasswordInstanceView.as_view(), name='passwords_api_instance'),
)