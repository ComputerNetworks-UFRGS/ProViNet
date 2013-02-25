from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'provinet.views.home', name='home'),
    # url(r'^provinet/', include('provinet.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
  
    # New urls - include app in ALPHABETICAL ORDER within its package
    
    url(r'^$', 'provinet.views.index'),
    
    # Development
    url(r'^dashboard/', include('provinet.development.dashboard.urls')),
    url(r'^services/', include('provinet.development.services.urls')),
    url(r'^modules/', include('provinet.development.modules.urls')),
    
    # Core
    url(r'^accounts/', include('provinet.core.accounts.urls')),
    url(r'^projects/', include('provinet.core.projects.urls')),
    url(r'^memberships/', include('provinet.core.memberships.urls')),
    
    # Infrastructure
     url(r'^slices/', include('provinet.infrastructure.slices.urls')),
     url(r'^vips/', include('provinet.infrastructure.vips.urls')),

)

