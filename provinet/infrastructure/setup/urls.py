from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.setup.views',
    (r'^resource_pools$', 'index_resource_pools'),
    (r'^vips$', 'index_vips'),
    (r'^(?P<id>\d+)/delete$', 'delete'),
    (r'^new_vip/', 'newVIP'),
    (r'^new_resource_pool/', 'newResourcePool'),
)
