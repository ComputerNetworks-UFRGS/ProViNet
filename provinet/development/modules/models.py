from django.db import models
from provinet.infrastructure.control_clusters.models import Vendor


class Module (models.Model):
    
    vendor = models.ForeignKey(Vendor)
    base = models.CharField(max_length=1024, null=False)
    wadl_file = models.FileField(upload_to='static/uploaded/dev', null=False)
    grammar_file = models.FileField(upload_to='static/uploaded/dev')
    
    def __unicode__ (self):
        return self.base
