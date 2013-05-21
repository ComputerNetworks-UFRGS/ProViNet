from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.development.applications.views',
    (r'^(?P<project_id>\d+)/$', 'index'),
    (r'^new/(?P<project_id>\d+)/$', 'new'),
    (r'^save/(?P<project_id>\d+)/$', 'save'),
    (r'^delete/(?P<project_id>\d+)/$', 'delete'),
    (r'^get/(?P<project_id>\d+)/$', 'get'),
    (r'^run/(?P<project_id>\d+)/$', 'run')
)