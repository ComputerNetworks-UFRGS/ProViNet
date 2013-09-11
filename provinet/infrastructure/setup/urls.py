from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.setup.views',
    (r'^resource_pools$', 'index_resource_pools'),
    (r'^new_resource_pool/', 'newResourcePool'),
    (r'^(?P<resourcepool_id>\d+)/resource_pool/delete$', 'deleteResourcePool'),
    (r'^(?P<resourcepool_id>\d+)/resource_pool/update$', 'updateResourcePool'),
    
    (r'^vips$', 'index_vips'),
    (r'^new_vip/', 'newVIP'),
    (r'^(?P<vip_id>\d+)/vip/delete$', 'deleteVIP'),
    (r'^(?P<vip_id>\d+)/vip/update$', 'updateVIP'),
)
