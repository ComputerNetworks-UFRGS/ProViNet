from django.db import models
from provinet.core.projects.models import Project

"""
The classes below are used to map WADL resources. More
information at: http://www.w3.org/Submission/wadl/
"""

class Applications (models.Model):
    
    name = models.CharField(max_length=255, null=False)
    project = models.ForeignKey(Project)
    language = models.CharField(max_length=255, null=False)
    working = models.TextField()
    
    def __unicode__ (self):
        return self.name