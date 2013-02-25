from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from provinet.infrastructure.slices.models import Slice

@login_required
def dashboard (request, project_id) :
    s = Slice.objects.filter(project_id=project_id)
    return render_to_response('application/dashboard/dashboard.html', RequestContext(request, {'slice': s}))