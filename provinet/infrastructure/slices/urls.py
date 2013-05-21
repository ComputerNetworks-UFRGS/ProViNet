from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.slices.views',
    (r'^(?P<project_id>\d+)/$', 'show'),
    (r'^(?P<slice_id>\d+)/delete$', 'delete'),
    (r'^new/(?P<project_id>\d+)/$', 'new'),
    #(r'^new', 'new'),
    (r'^commit$', 'commit'),
    (r'^request_to_vip$', 'request_to_vip'),
)
