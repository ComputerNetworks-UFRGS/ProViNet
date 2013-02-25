from provinet.infrastructure.resource_pools.models import ControlCluster
from provinet.infrastructure.controllers.models import Controller
import XenAPI, time, logging
from django.contrib import messages
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

def xenSession(url, username, password):
    """
    Start XenServer session
    """
    session = XenAPI.Session(url)
    session.xenapi.login_with_password(username, password)
    return session

def read_ip_address(session, vm):
        vgm = session.xenapi.VM.get_guest_metrics(vm)
        try:
            os = session.xenapi.VM_guest_metrics.get_networks(vgm)
            if "0/ip" in os.keys():
                return os["0/ip"]
            return None
        except:
            return None

def requestVM(new_name, amount, name, plane):
    """
    Clone a pre-existent virtual machine at XenServer.
    @new_name is the name of the new VM
    @amount number of machines to be created
    @name name of the virtual machine pre-configured at the resource pool that will be cloned
    if the plane is "control" the @name is not necessary, once the vm_base name can be found in
    the ControlPlane model.
    @plane accordingly to ProViNet architecture, it can be "execution" or "control"
    """
    
    virtual_machines_ips = []
    new_vm_list = []
    
    # Read configurations
    resource_pool = ControlCluster.objects.filter(is_active=True)[:1].get()
    if resource_pool:
        name = resource_pool.vm_base
    else:
        logger.error("ERROR: Neither 'control', nor 'execution' were used as parameter.")
        return False
    
    username, password, url = resource_pool.username, resource_pool.password, resource_pool.url
    # ---
    
    # Start Session
    session = xenSession(url, username, password)
    
    # Name label of the VM to be cloned
    vm_base = session.xenapi.VM.get_by_name_label(name)[0]
    
    # Cloning and starting VMs
    t_clone = time.time()
    for i in range(int(amount)):
        print "Cloning VM %i ..." % i
        vm_new_obj = session.xenapi.VM.clone(vm_base, (new_name + "-" + str(i)))
        session.xenapi.VM.start(vm_new_obj, False, True)
        new_vm_list.append(vm_new_obj)
    print "time cloning = %s " % str(time.time()-t_clone)
    
    # Reading IP addresses of VMs created
    t_boot = time.time()
    m = 0
    for j in new_vm_list:
        print "VM %i is booting ..." % m
        m += 1
        while read_ip_address(session, j) == None: time.sleep(1)
        ip = read_ip_address(session, j)
        virtual_machines_ips.append(ip)
    print "time booting = %s " % str(time.time()-t_boot)


    # Store Controller Informations
    if plane == "control":
        for j in range(len(virtual_machines_ips)):
            # saving information
            ctl = Controller()
            ctl.technology_name = "Floodlight"
            ctl.status = True
            ctl.control_plane = resource_pool
            ctl.address = virtual_machines_ips[j]
            ctl.username = "ubuntu"
            ctl.password = "q1w2e3"
            ctl.save()

    return virtual_machines_ips
