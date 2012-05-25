from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import PasswordForm

def password_list(request):
    context = RequestContext(request)
    form = PasswordForm()
    context.update({'form': form})
    return render_to_response('passwords/password_list.html', context)