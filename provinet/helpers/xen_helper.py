from provinet.infrastructure.setup.models import ResourcePool
import XenAPI, time, logging

logger = logging.getLogger(__name__)

def xenSession():
    """
    Start XenServer session
    """
    
    # Retrieve resource pool configurations
    resource_pool = ResourcePool.objects.filter(status=True)[:1].get()
    if resource_pool:
        global name
        name = resource_pool.vm_name
        username, password, url = resource_pool.username, resource_pool.password, resource_pool.uri
    else:
        logger.error("ERROR: There is no Resource Pool configured.")
        return False
    # ---
    
    
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

def getStatus(vm_name):
    '''
    Get power status of the virtual machine "running", "halted"...
    '''
    
    # Start Session
    try:
        session = xenSession()
    except:
        return False
    
    vm = session.xenapi.VM.get_by_name_label(vm_name)[0]
    record = session.xenapi.VM.get_record(vm)

    return record["power_state"]

def deleteVM(vm_name):
    '''
    This function deletes a vm at XenServer.
    Deleting vm by name is not safe, it need to be improved.
    '''
    
    # Start Session
    try:
        session = xenSession()
    except:
        return False
    
    # Name label of the VM to be deleted
    vm_obj = session.xenapi.VM.get_by_name_label(vm_name)[0]
    
    # Shutdown
    print "VM shutdown..."
    session.xenapi.VM.clean_shutdown(vm_obj)
    
    # Destroy
    print "VM Destroy..."
    try:
        session.xenapi.VM.destroy(vm_obj)
    except:
        print "Could not destroy VM"
        return False

    session.xenapi.session.logout()

def requestVM(new_name):
    """
    Clone a pre-existent virtual machine at XenServer.
    @new_name name label of cloned vm
    return a list of ips or False when there is no resource pool configured
    """
    amount = 1 # Possible implementation of many instances per request
    virtual_machines_ips = [] # <string>
    vm_list = [] # <vm object>
    
    # Start Session
    try:
        session = xenSession()
    except:
        return False
    
    global name
    # Name label of the VM to be cloned
    vm_name = session.xenapi.VM.get_by_name_label(name)[0]
    
    # Cloning and starting VMs
    t_clone = time.time()
    for i in range(int(amount)):
        print "Cloning VM %i ..." % i
        vm_new_obj = session.xenapi.VM.clone(vm_name, new_name)
        session.xenapi.VM.start(vm_new_obj, False, True)
        vm_list.append(vm_new_obj)
    print "time cloning = %s " % str(time.time()-t_clone)
    
    # Reading IP addresses of VMs created
    t_boot = time.time()
    m = 0
    for j in vm_list:
        print "VM %i is booting ..." % m
        m += 1
        while read_ip_address(session, j) == None: time.sleep(1)
        ip = read_ip_address(session, j)
        virtual_machines_ips.append(ip)
    print "time booting = %s " % str(time.time()-t_boot)
    
    session.xenapi.session.logout()
    
    # return an <array of String>
    return virtual_machines_ips
