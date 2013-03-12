from django.db import models
from provinet.core.projects.models import Project

class Vendor (models.Model):
    """
    An OpenFlow Controller vendor (Ex.: FloodLight, Trema, Nox)
    """
    name = models.CharField(max_length=100, null=False)
    version = models.CharField(max_length=50, null=True)
    
    def __unicode__ (self):
        return self.name
    
class ResourcePool (models.Model):
    name = models.CharField(max_length = 100)
    uri = models.CharField(max_length = 200, null=False)
    username = models.CharField(max_length = 30, null=False)
    password = models.CharField(max_length = 100, null=False)
    vm_name = models.CharField(max_length = 30, null=False)
    
    def __unicode__ (self):
        return self.name

class ControlCluster (models.Model):
    project = models.OneToOneField(Project)
    vendor = models.ForeignKey(Vendor)
    resource_pool = models.ForeignKey(ResourcePool, null=False)
    redundancy = models.IntegerField(null=False)
    
    def __unicode__ (self):
        return "Cluster"