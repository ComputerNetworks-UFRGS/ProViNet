from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.control_clusters.views',
    (r'^$', 'index'),
    (r'^(?P<pj_id>\d+)/$', 'show'),
    (r'^vendor/(?P<vendor_id>\d+)/$', 'showVendor'),
    (r'^vendor/new/$', 'newVendor'),
    (r'^vendor/delete/(?P<vendor_id>\d+)/$', 'deleteVendor'),
)
