from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms import ModelForm
from provinet.infrastructure.setup.models import ResourcePool

@login_required
def index (request):
    return render_to_response('infrastructure/setup/index.html', RequestContext(request,))

class CreationForm(ModelForm):
    
    class Meta:
        model = ResourcePool
        
        
def new (request, project_id):
    """
    Create a new resource pool
    """
    
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource Pool successfully created!")
            return HttpResponseRedirect('/projects/%s' % project_id)
    else:
        form = CreationForm()
        return render_to_response('infrastructure/setup/new.html', RequestContext(request, {'form': form,'project_id': project_id, }))



def delete (request, resourcepool_id):
    if request.method == 'GET':
        rp = ResourcePool.objects.filter(id=resourcepool_id)
        if rp.exists():
            rp.delete()
            messages.success(request, "Resource Pool successfully deleted!")
            return HttpResponseRedirect('/projects/')
        else:
            messages.success(request, "Resource Pool not found!")
            return HttpResponseRedirect('/projects/')
    

