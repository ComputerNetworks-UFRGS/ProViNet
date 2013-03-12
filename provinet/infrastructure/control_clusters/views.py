from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms import ModelForm
from provinet.infrastructure.control_clusters.models import ControlCluster
from provinet.infrastructure.setup.models import ResourcePool
from provinet.core.projects.models import Project

class newControlClusterForm(ModelForm):
    class Meta:
        model = ControlCluster
        exclude = ('resource_pool','project')


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
            messages.success(request, "Control Cluster successfully created!")
            return HttpResponseRedirect('/projects/%s' % project_id)

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
    