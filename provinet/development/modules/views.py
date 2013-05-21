from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib import messages
from xml.etree.ElementTree import ElementTree
from provinet.development.modules.models import Module
from provinet.development.services.models import Service, Method, Param
from provinet.infrastructure.control_clusters.models import Vendor

@login_required
def index (request):
    return render_to_response('development/modules/index.html', RequestContext(request,))


def getET(file_path):
    return 

def getBaseURI(ET):
    # Find the base url of <resources base="http://..." />
    resources = ET.findall('resources')[0]
    return resources.get('base')

def parseWADL(ET, moduleobj):
    '''
    This parser aims at parsing a WADL file to ProViNet database model. This parcer follows the WADL standard
    definition provided in http://www.w3.org/Submission/wadl/.
    The services description (WADL) of many famous web service providers can be found at:
    https://github.com/apigee/wadl-library
    '''
    
    resources = ET.findall('resources')[0]
    # Find services available and add to database
     
    # Iterate resources and get available services
    for resource in resources.getchildren():
        service_uri = resource.get('path')
        serviceobj = Service.objects.create(module=moduleobj, path=service_uri, description='')
        
        # Iterate resource and get html Methods (GET, POST...) available for this service
        for method in resource.findall('method'):
            methodobj = Method.objects.create(method_id=method.get('id'), name=method.get('name'), service=serviceobj)

        # Iterate resource to get params. Either GET (news/{new_id}) or POST params
        for param in resource.findall('param'):
            try:
                type_value = param.get('type')
            except:
                type_value = ' '

            # Get pre-defined values, if any
            values = ' '
            for option in param.getchildren():
                values += option.get('value')+';'
            Param.objects.create(name = param.get('name'), style = param.get('style'), values = values,
                                  type = type_value, is_required = True, method = methodobj, service = serviceobj)

    return "WADL successfully parsed!"

class NewModuleForm (ModelForm):
    class Meta():
        model = Module
        exclude = ('base','vendor',)

def new (request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
     
    if request.method == 'POST':
        form = NewModuleForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
           
            obj.vendor = vendor

            obj.save() # in order to upload the file 
            
            print 'file at:' + 'media/'+str(obj.wadl_file)
            print 'file_url at:' + str(obj.wadl_file.url)
            try:
                ET = ElementTree("application", (str(obj.wadl_file.url)))  # Transform xml file to Element Tree object
            except Exception, e:
                messages.error(request, "Parse Failed! Error loading wald.\n %s" % str(e))
                return HttpResponseRedirect('/control_clusters/vendor/%s/' % str(vendor_id))
            
            obj.base = getBaseURI(ET)  # Retrieve base uri of wadl
            module = form.save()
            print 'salvou modulo'
            
            # Trigger the parser to retrieve services from wadl
            response = parseWADL(ET, module)
            if response.split(' ')[0] == 'ERROR!':
                messages.error(request, "Parse Failed! Check your wadl syntax. Error: %s" % response)
                return HttpResponseRedirect('/projects/')
            
            # Trigger the update of template () to show services accordingly
            
            messages.success(request, "Module successfully created.")
            return HttpResponseRedirect('/control_clusters/vendor/%s/' % str(vendor_id))
    else:
        form = NewModuleForm()
        # return render(request, 'slices/upload_file/upload.html', {'form': form})
    return render_to_response('development/modules/new.html', RequestContext(request, {'form':form, 'vendor':vendor}))
