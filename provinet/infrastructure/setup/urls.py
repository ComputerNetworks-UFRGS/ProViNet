from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.setup.views',
    (r'^$', 'index'),
    (r'^(?P<id>\d+)/delete$', 'delete'),
    (r'^new_vip/', 'newVIP'),
    (r'^new_resource_pool/', 'newResourcePool'),
)
