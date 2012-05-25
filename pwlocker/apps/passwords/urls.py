from django.conf.urls.defaults import patterns, url

from models import Password

urlpatterns = patterns('apps.passwords.views',
    url(r'^$', 'password_list', name='password_list'),
)