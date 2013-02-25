from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from provinet.infrastructure.slices.models import Slice
from provinet.infrastructure.vips.models import VIP
from provinet.helpers import xen_helper
from xml.etree.ElementTree import ElementTree, Element, SubElement
import urllib, httplib, time

@login_required
def index (request):
    return render_to_response('infrastructure/slices/index_slices.html', RequestContext(request,))

class UploadFileForm(ModelForm):
    
    class Meta:
        model = Slice
        exclude = ('is_commited','project',)

def new (request):
    """
    Create in DB a new slice and store the VXDL uploaded into static/uploaded/.
    """
    if request.method == 'POST':
        t0 = time.time()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully uploaded in %s seconds" % (time.time() - t0))
            return HttpResponseRedirect('/projects/')
    else:
        form = UploadFileForm()
        return render_to_response('infrastructure/slices/new.html', RequestContext(request, {'form': form}))
    

def newControllerElement(conn_type, ip, port, tp):
    """
    Creates the XML Element controller, with its atrributes, conn_type, ip and port
    The result in file would be:
    <controller type="tp">
      <connection_type>conn_type</connection_type>
      <ipAddress>ip</ipAddress>
      <port>port</port>
    </controller>
    """
    controller = Element("controller", type=tp)
    conn = SubElement(controller, "connection_type")
    conn.text = conn_type
    
    ipadd = SubElement(controller, "ipAddress")
    ipadd.text = ip
    
    prt = SubElement(controller, "port")
    prt.text = port
    
    return controller

def parsePVNDL(controllers_ips, path_to_file):
    """
    Edit the VXDL document uploaded by the user adding controller informations.
    @path_to_file is where ProViNet stored the VXDL file uploaded by the user
    """
    DEFAULT_CTL_PORT = "6633"
    DEFAULT_CTL_CONN = "tcp"
    # Creates an ET Object from the VXDL file
    ET = ElementTree("virtualInfrastructure", path_to_file)
    # Find the root
    root = ET.getroot()
    # Create a new Element controllerList
    cList = Element("controllerList", id="controllerSet")
    
    # Add the controllers ip to the XML. If there are more than 1 controller, the 1st is 'master' and the others, 'slave'
    for j in range(len(controllers_ips)):
        controller = newControllerElement(DEFAULT_CTL_CONN, controllers_ips[j],
                                   DEFAULT_CTL_PORT, ("master" if j == 0 else "slave"))
        cList.append(controller)
    # Append the <controllerList/> to the root element of XML file
    root.append(cList)
    
    # Set the <controlPlane> text of all vRouter in the file
    for vrouter in root.findall('vRouter'):
        vrouter.find('controlPlane').text = "controllerSet"

    # Saving
    ET.write(path_to_file, "us-ascii", None, None, "xml")

    return "The file " + path_to_file + " PVNDL parsed with no errors!"

@csrf_exempt
def commit(request):
    """
    The request comes from ajax_funcions.js and require the efective creation of a slice
    Two steps are needed, see below
    """
    controllers_ips=[]
    project_id = request.POST['project_id']
    if request.is_ajax():
        if request.method == 'POST':
            # POST values
            redundancy = request.POST['redundancy']
            vxdl_file_path = request.POST['path']
            
            # ID base for controller VMs
            identity = "ctl-usr-"+str(request.user.id)+"-prj-"+project_id

            # 1st STEP - Request controllers virtual machines from the Control Plane. requestVM() from provinet.helper ---
            print "Requesting Controllers..."
            t_control = time.time()
            controllers_ips = xen_helper.requestVM(identity, redundancy, "", "control")
            print "Time to create controllers = %s " % str(time.time()-t_control)
            # --------------
            
            # 2nd STEP - Edit the VXDL file adding controllers informations
            t_edit = time.time()
            message = parsePVNDL(controllers_ips, vxdl_file_path)
            print ("Time to edit VXDL = %s " % str(time.time()-t_edit))
            
#            # --- Add a new subdomain in the DNS Server
#            project = Project.objects.get(id=project_id)
#            subdomain = project.title.lower()
#            control_plane = ControlPlane.objects.filter(is_active=True)[:1].get()
#            for c in control_plane.controller_set.all():
#                controllers_ips.append(c.address)
#            dns_helper.addSubdomain(subdomain, controllers_ips)
#            #---- Save the control plane reference for further access -----------
#            project.control_plane_url = subdomain+".provinet.local"
#            project.save()
            #----------
            message += "\n Success!"
    else:
        message = "Error in AJAX request. Please activate javascript in your browser"
    return HttpResponse(message)

@csrf_exempt
def request_to_vip(request):
    """
    This function send a request (VXDL document) to a Virtual Infrastructure Provider pre configured in
    vips.model. The request can be sent using different protocols.
    """
    debug = False
    if debug == False:
        if request.is_ajax():
            if request.method == 'POST':
                slice_id = request.POST['slice_id']
                
                # Read vxdl file to string
                vxdl_file = open(request.POST['path'], 'r+')
                vxdl_str = vxdl_file.read();
                
                # Get vip configured
                active_vip = VIP.objects.filter(is_active=True)
                if len(active_vip) == 0:
                    return HttpResponse("There is no Virtual Infrastructure Providers configured!")

                active_vip = active_vip[0]
                
                # Creates POST dictionary properly encoded
                params = urllib.urlencode({'name': ('provinet-'+slice_id), 'vxdl_file': vxdl_str})
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

                if active_vip.protocol == "http":
                    try :
                        conn = httplib.HTTPConnection(active_vip.host_address)
                    except :
                        return HttpResponse("Sorry! The Infrastructure Provider "+ active_vip.title
                                            +" is offline. \n Try again Later.")
                else:
                    return HttpResponse("SLICE REQUEST ERROR: Just HTTP connections are supported by now!")
                
                conn.request(active_vip.method, active_vip.host_path, params, headers)
                response = conn.getresponse()
                message = "Answer of "+active_vip.title+": \n"+response.read()
                
                # Change status of slice to Commited
                sl = Slice.objects.get(id=slice_id)
                sl.is_commited = True
                sl.save()
        else:
            message = "Error in AJAX request. Please activate javascript in your browser"
    else:
        message = "Request to VIP passed!"
    return HttpResponse(message)
