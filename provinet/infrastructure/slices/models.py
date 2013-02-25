from django.db import models
from provinet.infrastructure.vips.models import VIP
from provinet.core.projects.models import Project

class Slice (models.Model):
    name = models.CharField(max_length=100)
    project = models.OneToOneField(Project)
    desc_file = models.FileField(upload_to='static/uploaded/infstr', null=False)
    vip = models.ForeignKey(VIP, null=False)
    is_commited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __unicode__ (self):
        return self.name
