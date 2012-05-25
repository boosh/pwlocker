from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from models import Password

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Password), name='password_list'),
)