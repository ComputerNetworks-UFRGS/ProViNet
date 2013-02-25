from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.template import RequestContext
from provinet.core.projects.models import Project
from provinet.core.memberships.models import Membership
from django.forms.models import ModelForm
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required
def index (request):
    """
    Return a html page with a list of Projects
    """
    p = Project.objects.all()
    return render_to_response('core/projects/index.html', RequestContext(request, {'projects': p}))
