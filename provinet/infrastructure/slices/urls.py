from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.slices.views',
    (r'^$', 'index'),
    (r'^new', 'new'),
    (r'^commit', 'commit'),
    (r'^request_to_vip', 'request_to_vip'),
)
