from django.contrib import admin
from provinet.infrastructure.setup.models import VIP, ResourcePool

admin.site.register(VIP)
admin.site.register(ResourcePool)