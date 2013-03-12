from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def index (request):
    return render_to_response('development/applications/index.html', RequestContext(request,))

def new (request):
    return render_to_response('development/applications/new.html', RequestContext(request,))
