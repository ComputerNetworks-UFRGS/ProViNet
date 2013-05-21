from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.forms import ModelForm
from provinet.infrastructure.control_clusters.models import ControlCluster, Vendor
from provinet.infrastructure.setup.models import ResourcePool
from provinet.core.projects.models import Project

def index (request):
    cc = ControlCluster.objects.all()
    vr = Vendor.objects.all()
    return render_to_response('infrastructure/control_clusters/index.html',
                              RequestContext(request, {"control_clusters": cc, 'vendors' : vr}))

def show (request, pj_id):
    prj = Project.objects.get(id=pj_id)
    return render_to_response('infrastructure/control_clusters/show.html', RequestContext(request, {"project": prj}))

def showVendor (request, vendor_id):
    vr = Vendor.objects.get(id=vendor_id)
    return render_to_response('infrastructure/control_clusters/vendor/show.html', RequestContext(request, {"vendor": vr}))


class newControlClusterForm(ModelForm):
    class Meta:
        model = ControlCluster
        exclude = ('resource_pool', 'project')


def newControlCluster (request, project_id):
    """
    Create a new control cluster
    """

    if request.method == 'POST':
        cc = newControlClusterForm(request.POST, prefix='cc')
        if cc.is_valid():
            obj = cc.save(commit=False)
            pj = Project.objects.get(id=project_id)
            if len(ResourcePool.objects.filter(status=True)) > 0:
                rp = ResourcePool.objects.filter(status=True)[0]
                obj.resource_pool = rp
            else:
                return False
            obj.project = pj
            cc.save()
            
            return HttpResponseRedirect('/projects/%s' % project_id)

class newVendorForm(ModelForm):
    class Meta:
        model = Vendor

def newVendor (request):
    """
    Register a new vendor in the system
    """
    
    if request.method == 'POST':
        cc = newVendorForm(request.POST)
        if cc.is_valid():
            cc.save()
            messages.success(request, "Vendor registred successfully!")
            return HttpResponseRedirect('/control_clusters/')
    else:
        form = newVendorForm()
        return render_to_response('infrastructure/control_clusters/vendor/new.html', RequestContext(request, {'form': form }))

def deleteVendor (request, vendor_id):
    """
    Delete vendor
    """
    if request.method == 'GET':
        cc = Vendor.objects.filter(id=vendor_id)
        if cc.exists():
            cc.delete()
            messages.success(request, "Vendor Successfully deleted!")
            return HttpResponseRedirect('/control_clusters/')
        else:
            messages.success(request, "Vendor not found!")
            return HttpResponseRedirect('/control_clusters/')

def delete (request, controlcluster_id):
    """
    When the user request a slice deletion, both the local db reference and 
    remote (in the vip) need to be deleted
    """
    if request.method == 'GET':
        cc = ControlCluster.objects.filter(id=controlcluster_id)
        if cc.exists():
            cc.delete()
            messages.success(request, "Control Cluster Successfully deleted!")
            return HttpResponseRedirect('/projects/')
        else:
            messages.success(request, "Slice not found!")
            return HttpResponseRedirect('/projects/')
    
