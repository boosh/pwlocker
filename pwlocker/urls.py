from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# dynamically import the user form module based on the project name
user_forms = __import__(str(settings.PROJECT) +  ".apps.users.forms",
    globals(), locals(), ['UserRegistrationForm', 'EmailAuthenticationForm'], -1)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', str(settings.PROJECT) + '.views.home', name='home'),

    url(r'^passwords/', include('apps.passwords.urls')),
    url(r'^api/1.0/', include('apps.api.urls')),

    # override the default log-in form
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {
        'authentication_form': user_forms.EmailAuthenticationForm}),

    (r'', include('django.contrib.auth.urls')),

    # override the default registration form
    url(r'^accounts/register/$', 'registration.views.register', {
        'backend': 'registration.backends.simple.SimpleBackend',
        'success_url': settings.LOGIN_REDIRECT_URL,
        'form_class': user_forms.UserRegistrationForm },
        name='registration_register'),

    (r'^accounts/', include('registration.backends.simple.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
