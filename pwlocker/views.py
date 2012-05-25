from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

## The home page.
def home(request):
    context = RequestContext(request)
    return render_to_response('base.html', context)