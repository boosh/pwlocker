from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from apps.users.forms import UserRegistrationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', str(settings.PROJECT) + '.views.home', name='home'),

    url(r'^passwords/', include('apps.passwords.urls')),
    url(r'^api/1.0/', include('apps.api.urls')),

    # override the default log-in form
    (r'^accounts/login$', 'django.contrib.auth.views.login'),

    (r'', include('django.contrib.auth.urls')),

    # override the default registration form
    url(r'^accounts/register/$', 'registration.views.register', {
        'backend': 'registration.backends.simple.SimpleBackend',
        'form_class': UserRegistrationForm,
        'success_url': settings.LOGIN_REDIRECT_URL },
        name='registration_register'),

    (r'^accounts/', include('registration.backends.simple.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
