from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.core.projects.views',
    (r'^$', 'index'),
    (r'^(?P<project_id>\d+)/$', 'show'),
    (r'^new', 'new'),
)
