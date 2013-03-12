from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.controllers.views',
    (r'^(?P<controller_id>\d+)/(?P<project_id>\d+)/delete$', 'delete'),
    (r'^new/(?P<cc_id>\d+)/(?P<project_id>\d+)$', 'new'),
)
