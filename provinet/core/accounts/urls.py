from django.conf.urls.defaults import *


urlpatterns = patterns('provinet.core.accounts.views',
    (r'^$', 'index'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    #(r'^$', 'django.contrib.auth.views.login', {'template_name':'users/login.html'}),
    #(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'users/login.html'}),
)


