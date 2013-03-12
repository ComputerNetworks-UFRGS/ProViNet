from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms import ModelForm
from provinet.infrastructure.controllers.models import Controller
from provinet.infrastructure.control_clusters.models import ControlCluster
from provinet.helpers import xen_helper
import time

class newControllerForm(ModelForm):
    class Meta:
        model = Controller
        exclude = ('control_cluster',)


def new (request, cc_id, project_id):
    """
    Create a new controller
    """
    
    # ID base for controller VMs
    identity = "ctl-usr-" + str(request.user.id) + "-prj-" + project_id

    #controller_ip = xen_helper.requestVM(identity)[0]
    controller_ip = "143.54.12.89"
    time.sleep(4)
    cc = ControlCluster.objects.get(id=cc_id)
    role_name = "master" if (len(ControlCluster.objects.filter())) == 0 else "slave"
    
    ctl = Controller.objects.create(control_cluster=cc, role=role_name, ip=controller_ip,
                                    port=6633, username="ubuntu", password="q1w2e3")
    # --------------
    # obj = ctl.save(commit=False)
    # cc = ControlCluster.objects.get(id=cc_id)
    # obj.control_cluster = cc
    # ctl.save()
    messages.success(request, "Controller successfully created!")
    return HttpResponseRedirect('/projects/%s' % project_id)

def delete (request, controller_id, project_id):
    """
    Delete a controller
    """
    # TODO: Call DeleteVM() from xen_helper.py (which is not created yet)
    if request.method == 'GET':
        ctl = Controller.objects.filter(id=controller_id)
        if ctl.exists():
            ctl.delete()
            messages.success(request, "Controller Successfully deleted!")
            return HttpResponseRedirect('/projects/%s' % project_id)
        else:
            messages.success(request, "Controller not found!")
            return HttpResponseRedirect('/projects/%s' % project_id)
    
