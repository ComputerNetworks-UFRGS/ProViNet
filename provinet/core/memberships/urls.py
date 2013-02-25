from django.conf.urls.defaults import *

urlpatterns = patterns('provinet.core.memberships.views',
    (r'^$', 'index'),
)
