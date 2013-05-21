from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from provinet.core.projects.models import Project
from provinet.development.applications.models import Applications
from provinet.development.services.models import Method
import json, httplib, urllib, re

@login_required
def index (request, project_id):
    prj = Project.objects.get(id=project_id)
    return render_to_response('development/applications/index.html', RequestContext(request, {'project' : prj}))

def new (request, project_id):
    prj = Project.objects.get(id=project_id)
    # Edit javascript jsBox
    return render_to_response('development/applications/new.html', RequestContext(request, {'project' : prj}))

@csrf_exempt
def save (request, project_id):
    if request.method == 'POST':
        # Load json request to object
        data = json.loads(request.raw_post_data)
        name = data.get('params').get('name')
        language = data.get('params').get('language')
        working = data.get('params').get('working')
        
        # Find project
        project_id = data.get('project_id')
        project = Project.objects.get(id=project_id)

        # Check if is a new app or update
        response = Applications.objects.filter(project=project, name=name, language=language)
        if not (len(response) == 0):
            response[0].working = working
            response[0].save()
        else:
            newapp = Applications.objects.create(project=project, name=data.get('params').get('name'),
                                              language=data.get('params').get('language'),
                                              working=data.get('params').get('working'))
    
    response_data = {}
    response_data['result'] = 'Success'
    response_data['error'] = None
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def delete (request, project_id):
    print "deleted"
    print request
    return HttpResponse("{'success' : 'true'}")

def get (request, project_id):
    project = Project.objects.get(id=project_id)
    apps = Applications.objects.filter(project=project)
    
    response = []
    for app in apps:
        wire = {}
        wire['name'] = app.name
        wire['working'] = app.working
        wire['language'] = app.language
        response.append(wire)
        
    return HttpResponse(json.dumps(response), content_type="application/json")


def getNext (module_id):
    
    return False

@csrf_exempt
def run (request, project_id):
    
    if request.method == 'POST':
        params = request.POST.get("params", "0")
        data = json.loads(params)
        
        print params
        
        modules = data.get('working').get('modules')
        services_queue = []
        # search for start module id
        aux = 0
        start_id = -1
        for module in modules:
            services_queue.append(module)
            if module.get('name') == 'Start':
                start_id = aux
            aux += 1
        # if not found
        if start_id == -1:
            return HttpResponse("Error! Start not found. You need to wire up one Start module.")


        # Create execution queue
        wires = data.get('working').get('wires')
        execution_queue = []
        
        next = start_id
        for i in range(len(wires)):
            for wire in wires:
                if wire.get('src').get('moduleId') == next:
                    execution_queue.append(wire.get('tgt').get('moduleId'))
                    next = wire.get('tgt').get('moduleId')
                    break
        
        output = {}
        print 'BEFORE dispatcher'
        output = dispatcher(project_id, execution_queue, services_queue)
        print 'AFTER dispatcher'
        to_send = json.dumps(output)
        print to_send
        
    return HttpResponse(to_send, content_type="application/json")

def dispatcher (project_id, execution_queue, modules):
    
    output = '['
    # Get controller master
    project = Project.objects.get(id=project_id)
    controller = project.controlcluster.controller_set.filter(role='master')
    controller = controller[0]

    # Iterate the execution_queue that stores the index of modules[] with the module to dispatch.
    pos = 1
    for i in execution_queue:
        print 'exec queue = ' + str(execution_queue)
        print str(i)+' '+ modules[i].get('name')+' '+str(modules[i].get('value').get('title'))
        if modules[i].get('name') != 'Start' and modules[i].get('name') != 'Terminate':
            #print str(i)+" - entrou"
            process_to_run = Method.objects.get(method_id=modules[i].get('name'))
            if process_to_run.name == 'GET':
                #print ' == GET'
                get_param = modules[i].get('value').get('title')  # Params 'style=Template' see wadl definition
                if get_param != '' and get_param != None:
                    get_param = get_param.lower()
                else:
                    get_param = ''
                
                # TODO: Deal with multiple parameters with 'style=Template' such as /core/{switch_id}/{status}/json
                uri_to_call = process_to_run.service.path
                base = process_to_run.service.module.base

                # Create the path with param in place
                uri_to_call = re.sub("(\{[A-z]+\})", get_param, uri_to_call)
                
                headers = {"Content-type":"application/x-www-form-urlencoded", "Accept":"application/json"}
                try:
                    conn = httplib.HTTPConnection(controller.ip)
                    conn.request("GET", str(base + uri_to_call))
                    response = conn.getresponse()
                    string = response.read()
                except Exception, e:
                    js = {}
                    js['error'] = "Controller connection: " + str(e)
                    return js
                output += '{ "module" : "' + modules[i].get('name') + str(i) + '", "response" : '

                output += string + ('},' if (pos != len(execution_queue) - 1) else '}')
            
            if process_to_run.name == 'POST' or process_to_run.name == 'DELETE':
                print str(i)+" - entrou"
                keys = modules[i].get('value').keys() # Params post
                inline_param = {}
                for k in keys:
                    if not isinstance(modules[i].get('value').get(str(k)), dict):
                        value = modules[i].get('value').get(str(k))
                        if value != '':
                            inline_param[k] = value 
                        
                    elif isinstance(modules[i].get('value').get(str(k)), dict):
                        val = modules[i].get('value').get(str(k)).get('inputParams').get('value')
                        if val != '':
                            inline_param[k] = val 
                   
#                 for param in params:
#                     print param
#                     #inparams = aux.get('inputParams')
                    #print str(param) + ' ' + str(inparams)
                # TODO: Deal with multiple parameters with 'style=Template' such as /core/{switch_id}/{status}/json
                uri_to_call = process_to_run.service.path
                base = process_to_run.service.module.base
                
                # Creates POST dictionary properly encoded
                params = urllib.urlencode(inline_param)
                print inline_param
                print 'params= ',params,json.dumps(inline_param)
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
                print str(base + uri_to_call)
                try:
                    conn = httplib.HTTPConnection(controller.ip)
                    conn.request(process_to_run.name, str(base + uri_to_call), json.dumps(inline_param), headers)
                    response = conn.getresponse()
                    string = response.read()
                except Exception, e:
                    js = {}
                    js['error'] = "Controller connection: " + str(e)
                    return js
                output += '{ "module" : "' + modules[i].get('name') + str(i) + '", "response" : '
                print str(i),' < i - len >',len(execution_queue)
                output += string + ('},' if (pos != len(execution_queue) - 1) else '}')
            
        pos += 1
    output += "]"
    
    return output
