from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'provinet.development.dashboard.views.dashboard'),
)
