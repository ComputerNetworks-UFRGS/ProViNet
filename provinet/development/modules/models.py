from django.db import models
from provinet.infrastructure.control_clusters.models import Vendor


class Module (models.Model):
    
    vendor = models.ForeignKey(Vendor)
    base = models.CharField(max_length=1024)
    wadl_file = models.FileField(upload_to='documents/modules', null=False)
    grammar_file = models.FileField(upload_to='documents/modules')
    
    
    def get_wadl_file_name(self):
        if self.wadl_file:
            return str(self.wadl_file).split('/')[2]
        return None
    
    def get_grammar_file_name(self):
        if self.grammar_file:
            return str(self.grammar_file).split('/')[2]
        return None
    
    def __unicode__ (self):
        return self.base
