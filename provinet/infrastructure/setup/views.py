from django.shortcuts import render_to_response
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms import ModelForm
from provinet.infrastructure.setup.models import ResourcePool
from provinet.infrastructure.setup.models import VIP
from provinet.infrastructure.control_clusters.models import Vendor

@login_required
def index_resource_pools (request):
    rp = ResourcePool.objects.all()
    vr = Vendor.objects.all()
    return render_to_response('infrastructure/setup/index_resource_pools.html', RequestContext(request,{'resource_pools' : rp, 'vendors' : vr}))

def index_vips (request):
    vip = VIP.objects.all()
    vr = Vendor.objects.all()
    return render_to_response('infrastructure/setup/index_vips.html', RequestContext(request,{'vips' : vip, 'vendors' : vr}))

class NewResourcePoolForm(ModelForm):
    
    class Meta:
        model = ResourcePool
        
def newResourcePool (request):
    """
    Create a new resource pool
    """
    
    if request.method == 'POST':
        form = NewResourcePoolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource Pool successfully created!")
            return HttpResponseRedirect('/setup/resource_pools')
    else:
        form = NewResourcePoolForm()
        return render_to_response('infrastructure/setup/new_resource_pool.html', RequestContext(request, {'form': form, }))

class NewVIPForm(ModelForm):
    
    class Meta:
        model = VIP
        
def newVIP (request):
    """
    Create a new resource pool
    """
    
    if request.method == 'POST':
        form = NewVIPForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "VIP successfully created!")
            return HttpResponseRedirect('/setup/vips')
    else:
        form = NewVIPForm()
        return render_to_response('infrastructure/setup/new_vip.html', RequestContext(request, {'form': form, }))

class VIPUpdate(UpdateView):
    model = VIP
    fields = ['name','address','uri','location','protocol','method','is_active']
    template_name_suffix = '_update_form'
    

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
    

