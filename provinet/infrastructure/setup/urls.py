from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.setup.views',
    (r'^$', 'index'),
    (r'^(?P<id>\d+)/delete$', 'delete'),
    (r'^new/(?P<project_id>\d+)$', 'new'),
)
