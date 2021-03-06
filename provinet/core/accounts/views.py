from django.contrib import auth, messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def index(request):
    return render_to_response('core/accounts/login.html', RequestContext(request,))


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        messages.success(request, "Successfully login" )
        return HttpResponseRedirect('/projects/')
    else:
        # Show an message error
        #TODO: Show error when the user is not active
        messages.error(request, "Authentication failure. Your username and password didn't match. Please try again." )
        return HttpResponseRedirect('/')
    
def logout(request):
    auth.logout(request)
    messages.success(request, "Successfully logout" )
    return HttpResponseRedirect('/')