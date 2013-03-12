from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.development.applications.views',
    (r'^$', 'index'),
    (r'^new', 'new'),
)