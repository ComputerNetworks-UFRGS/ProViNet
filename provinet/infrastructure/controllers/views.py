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
    cc = ControlCluster.objects.get(id=cc_id)
    n_ctls = cc.controller_set.count()
    
    role_name = "master" if (n_ctls == 0) else "slave"
    
    # ID for controller VMs
    pos =  n_ctls + 1
    identity = "ctl-usr-" + str(request.user.id) + "-prj-" + project_id + "-" + str(pos)

    response = xen_helper.requestVM(identity)
    if response == False:
        messages.success(request, "Problem in the connection with the Resource Pool!")
        return HttpResponseRedirect('/projects/%s' % project_id)
    
    controller_ip = response[0]
    
    #controller_ip = "143.54.12.89"
    #time.sleep(4)
    
    Controller.objects.create(control_cluster=cc, name=identity, role=role_name, ip=controller_ip,
                                    port=6633, username="ubuntu", password="q1w2e3")
    # --------------
    
    messages.success(request, "Controller successfully created!")
    return HttpResponseRedirect('/projects/%s' % project_id)

def delete (request, controller_id, project_id):
    """
    Delete a controller
    """
    
    ctl = Controller.objects.get(id=controller_id)
    
    print "vm_name = "+ str(ctl.name)
    # Request deletion to XenServer (ControlCluster)
    xen_helper.deleteVM(ctl.name)
    
    if request.method == 'GET':
        ctl = Controller.objects.filter(id=controller_id)
        if ctl.exists():
            ctl.delete()
            messages.success(request, "Controller Successfully deleted!")
            return HttpResponseRedirect('/projects/%s' % project_id)
        else:
            messages.success(request, "Controller not found!")
            return HttpResponseRedirect('/projects/%s' % project_id)
    
