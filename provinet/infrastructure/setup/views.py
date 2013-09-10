from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms import ModelForm
from provinet.infrastructure.setup.models import ResourcePool
from provinet.infrastructure.setup.models import VIP
from provinet.infrastructure.control_clusters.models import Vendor

@login_required
def index (request):
    rp = ResourcePool.objects.all()
    vr = Vendor.objects.all()
    return render_to_response('infrastructure/setup/index.html', RequestContext(request,{'resource_pools' : rp, 'vendors' : vr}))

class NewResourcePoolForm(ModelForm):
    
    class Meta:
        model = ResourcePool
        exclude = ('status',)
        
def newResourcePool (request, project_id):
    """
    Create a new resource pool
    """
    
    if request.method == 'POST':
        form = NewResourcePoolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource Pool successfully created!")
            return HttpResponseRedirect('/projects/%s' % project_id)
    else:
        form = NewResourcePoolForm()
        return render_to_response('infrastructure/setup/new_resource_pool.html', RequestContext(request, {'form': form,'project_id': project_id, }))

class NewVIPForm(ModelForm):
    
    class Meta:
        model = VIP
        
def newVIP (request, project_id):
    """
    Create a new resource pool
    """
    
    if request.method == 'POST':
        form = NewVIPForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "VIP successfully created!")
            return HttpResponseRedirect('/projects/%s' % project_id)
    else:
        form = NewVIPForm()
        return render_to_response('infrastructure/setup/new_vip.html', RequestContext(request, {'form': form,'project_id': project_id, }))


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
    

