from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.development.modules.views',
    (r'^$', 'index'),
    (r'^new/(?P<vendor_id>\d+)/$', 'new'),
)