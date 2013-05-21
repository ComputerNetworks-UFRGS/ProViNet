from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.template import RequestContext
from django.forms.models import ModelForm
from django.contrib import messages
from django.http import HttpResponseRedirect

from provinet.core.projects.models import Project
from provinet.infrastructure.control_clusters.views import newControlCluster, newControlClusterForm
from provinet.core.memberships.models import Membership
from provinet.infrastructure.controllers.models import Controller
from provinet.helpers import xen_helper


@login_required
def index (request):
    """
    Return a html page with a list of Projects
    """
    p = Project.objects.all()
    return render_to_response('core/projects/index.html', RequestContext(request, {'projects': p}))

def show (request, project_id):
    p = Project.objects.get(id=project_id)
    
    # Update controllers status before show
    for c in p.controlcluster.controller_set.all():
        ctl = Controller.objects.get(id=c.id)
        ctl.status = xen_helper.getStatus(c.name)
        ctl.save()
    
    return render_to_response('core/projects/show.html', RequestContext(request, {'project': p}))

class newProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('members',)

def new (request):
    """
    Creates a new Project
    """
    if request.method == 'POST':
        pj = newProjectForm(request.POST, prefix='pj')
        if pj.is_valid():
            # Saving m2m relationship with User through Membership
            pjobj = pj.save()
            ownergp = Group.objects.get(id=1)
            Membership.objects.create(user=request.user, project=pjobj, group=ownergp)
            
            if newControlCluster(request, pjobj.id) == False:
                pjobj.delete()
                messages.error(request, "Error! Problem creating Project. No Resource Pool configured.")
                return HttpResponseRedirect('/projects/')
            else:
                messages.success(request, "The Project was successfully created")
                return HttpResponseRedirect('/projects/%s/' % (pjobj.id))
    else:
        formpj = newProjectForm(prefix='pj')
        formcc = newControlClusterForm(prefix='cc')
        return render_to_response('core/projects/new.html', RequestContext(request, {'formpj': formpj, 'formcc': formcc}))
