from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def index (request):
    return render_to_response('development/modules/index_modules.html', RequestContext(request,))

def new (request):
    if request.method == 'POST':
        print "oi"
        #form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            # instance = Slice(request.POST,file=request.FILES['file'])
            #form.save()
            #messages.success(request, "Successfully uploaded")
            #return HttpResponseRedirect('/dashboard/')
    else:
        #form = UploadFileForm()
        # return render(request, 'slices/upload_file/upload.html', {'form': form})
        return render_to_response('development/services/new_module.html', RequestContext(request,))
