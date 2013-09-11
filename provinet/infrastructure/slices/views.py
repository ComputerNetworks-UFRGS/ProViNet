from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from provinet.infrastructure.slices.models import Slice
from provinet.core.projects.models import Project
from provinet.infrastructure.setup.models import VIP
from provinet.helpers import xen_helper
from xml.etree.ElementTree import ElementTree, Element, SubElement
import urllib, httplib, time

@login_required
def show (request, project_id):
    prj = Project.objects.get(id=project_id)
    return render_to_response('infrastructure/slices/index.html', RequestContext(request, {'project':prj}))

class UploadFileForm(ModelForm):
    
    class Meta:
        model = Slice
        exclude = ('is_commited', 'project',)

def new (request, project_id):
    """
    Create a new slice entry and store the VXDL uploaded into static/uploaded/infstr/.
    """
    if request.method == 'POST':
        t0 = time.time()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            pj = Project.objects.get(id=project_id)
            obj.project = pj
            form.save()
            messages.success(request, "Slice description successfully uploaded!")
            return HttpResponseRedirect('/projects/%s/' % str(project_id))
    else:
        form = UploadFileForm()
        return render_to_response('infrastructure/slices/new.html', RequestContext(request, {'form': form, 'project_id': project_id, }))



def delete (request, slice_id):
    """
    When the user request a slice deletion, both the local db reference and 
    remote (in the vip) must be deleted
    """
    if request.method == 'GET':
        
        try:
            slice = Slice.objects.get(id=slice_id)
        except:
            messages.error(request, "Slice not found!")
            return HttpResponseRedirect('/projects/')

        # Request slice deletion to Virtual Infrastructure Provider
        # Get VIP configuration
        active_vip = VIP.objects.filter(is_active=True)
        if len(active_vip) == 0:
            return HttpResponse("There is no Virtual Infrastructure Providers configured!")

        active_vip = active_vip[0]
        

        # headers = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/plain"}

#         aux = 2  # Hardcoded
#         
#         conn = httplib.HTTPSConnection(active_vip.address)
#         conn.request("GET", "/HyFSManager/hyfs/slices/" + str(aux) + "/delete/")
        
#         response = conn.getresponse()
#         string = response.read()
#         
#         print string
        
        # Delete from uploaded/infstr/ the vxdl file
        slice.desc_file.delete()
        # Delete from database
        slice.delete()

        messages.success(request, "Slice Successfully deleted!")
        return HttpResponseRedirect('/projects/')
    
        
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

def parseVXDL(controllers_ips, path_to_file):
    """
    Edit the VXDL document uploaded by the user adding controller informations.
    @path_to_file is where ProViNet stored the VXDL file uploaded by the user
    """
    DEFAULT_CTL_PORT = "6633"
    DEFAULT_CTL_CONN = "tcp"
    # Creates an ET Object from the VXDL file
    
    try:
        ET = ElementTree("virtualInfrastructure", path_to_file)
    except Exception, e:
        return "ERROR! %s " % e 
    
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

    return "The file " + path_to_file + " PVNDL successfully parsed!"

@csrf_exempt
def commit(request):
    """
    The request comes from ajax_funcions.js and require the efective creation of a slice
    Two steps are needed, see below
    """
    controllers_ips = []
    
    if request.is_ajax():
        if request.method == 'POST':
            # POST values
            project_id = request.POST['project_id']
            prj = Project.objects.get(id=project_id)

            # get controller ips requested by the user
            
            ctls = prj.controlcluster.controller_set.all()
            for i in ctls:
                controllers_ips.append(i.ip)
                
            vxdl_file_path = request.POST['path']
            
            t_edit = time.time()
            message = parseVXDL(controllers_ips, vxdl_file_path)
            print ("Time to edit VXDL = %s " % str(time.time() - t_edit))
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
                
                # Get vip configuration
                active_vip = VIP.objects.filter(is_active=True)
                if len(active_vip) == 0:
                    return HttpResponse("There is no Virtual Infrastructure Providers configured!")

                active_vip = active_vip[0]

                # Creates POST dictionary properly encoded
                params = urllib.urlencode({'name': ('provinet-' + slice_id), 'vxdl_file': vxdl_str})
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

                try :
                    if active_vip.protocol == "http":
                        conn = httplib.HTTPConnection(active_vip.address)
                    elif active_vip.protocol == "https":
                        conn = httplib.HTTPSConnection(active_vip.address)
                    else:
                        return HttpResponse("SLICE REQUEST ERROR: Just HTTP and HTTPS connections are supported by now!")

                except :
                    return HttpResponse("Sorry! The Infrastructure Provider " + active_vip.name
                                            + " is offline. \n Try again Later.")

                conn.request(active_vip.method, active_vip.uri, params, headers)
                response = conn.getresponse()
                message = "Answer of " + active_vip.name + ": \n" + response.read()

                # Change status of slice to Commited
                sl = Slice.objects.get(id=slice_id)
                sl.is_commited = True
                sl.save()
        else:
            message = "Error in AJAX request. Please activate javascript in your browser"
    else:
        message = "Request to VIP passed!"
    return HttpResponse(message)
