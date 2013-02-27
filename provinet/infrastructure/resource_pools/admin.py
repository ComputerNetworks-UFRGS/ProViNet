from django.contrib import admin
from provinet.infrastructure.resource_pools.models import ResourcePool, ControlCluster, Vendor
from provinet.infrastructure.controllers.models import Controller
from provinet.development.modules.models import Module

class ControllerInline (admin.TabularInline):
    model = Controller

class ModuleInline (admin.TabularInline):
    model = Module

class ModuleAdmin (admin.ModelAdmin):
#    fieldsets = [
#        ('Poll Information', {'fields': ['question']}),
#        ('Date Information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
#    ]
    inlines = [ModuleInline]

class ControllerAdmin (admin.ModelAdmin):
#    fieldsets = [
#        ('Poll Information', {'fields': ['question']}),
#        ('Date Information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
#    ]
    inlines = [ControllerInline]
#    
#    list_filter = ['pub_date', 'end_date']
#    
#    list_display = ('question', 'end_date', 'was_published_today')
#    
#    search_fields = ['question']
#    
#    date_hierarchy = 'end_date'
    
#admin.site.register(ControlPlane)
admin.site.register(ControlCluster, ControllerAdmin)
admin.site.register(ResourcePool)
admin.site.register(Vendor, ModuleAdmin)