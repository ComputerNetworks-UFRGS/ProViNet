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

def show (request, project_id):
    p = Project.objects.get(id=project_id)
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
        pj = newProjectForm(request.POST)
        if pj.is_valid():
            # Saving m2m relationship
            # 1 get POST values
            nameValue = request.POST['name']
            is_publicValue = request.POST['is_public']
            # 2 create project with POST data
            pjobj = Project.objects.create(name=nameValue,is_public=is_publicValue)
            # 3 create membership entry with extra field group
            ownergp = Group.objects.get(id=1)
            Membership.objects.create(user=request.user, project=pjobj, group=ownergp)
            
            messages.success(request, "The Project was successfully created")
            return HttpResponseRedirect('/projects/%s/'% (pjobj.id))
    else:
        formpj = newProjectForm()
        return render_to_response('core/projects/new.html', RequestContext(request, {'formpj': formpj}))
