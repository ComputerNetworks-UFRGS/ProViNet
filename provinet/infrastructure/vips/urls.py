from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.infrastructure.vips.views',
    (r'^$', 'index'),
)
