from django.conf.urls.defaults import patterns, url

from views import PasswordListView, PasswordInstanceView
from views import PasswordContactListView, PasswordContactReadOrDeleteInstanceView
from views import UserView

urlpatterns = patterns('',
    url(r'^passwords/$', PasswordListView.as_view(), name='passwords_api_root'),
    url(r'^passwords/(?P<id>[0-9]+)$', PasswordInstanceView.as_view(), name='passwords_api_instance'),
    url(r'^passwordcontacts/$', PasswordContactListView.as_view(),
        name='password_contacts_api_root'),
    url(r'^passwordcontacts/(?P<id>[0-9]+)$', PasswordContactReadOrDeleteInstanceView.as_view(),
        name='password_contacts_api_instance'),
    url(r'^user/(?P<username>.+)$', UserView.as_view(), name='user_api'),
)