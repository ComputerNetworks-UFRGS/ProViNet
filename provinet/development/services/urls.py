from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.development.services.views',
    (r'^$', 'index'),
    (r'^new', 'new'),
)