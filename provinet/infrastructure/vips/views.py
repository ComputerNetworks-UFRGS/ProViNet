from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def index (request):
    return render_to_response('infrastructure/vips/index.html', RequestContext(request,))
