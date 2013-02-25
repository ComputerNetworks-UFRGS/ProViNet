from django.db import models
from provinet.infrastructure.resource_pools.models import ControlCluster

class Controller (models.Model):
    """
    This model represents an OpenFlow Controller instance
    """
    
    ROLES = (
           ('master','Master'),
           ('slave','Slave'),
           ('equal','Equal')
           )
    
    control_cluster = models.ForeignKey(ControlCluster)
    role = models.CharField(max_length=5, choices=ROLES)
    ip = models.CharField(max_length=15)
    port = models.CharField(max_length=10, default="8080")
    username = models.CharField(max_length=25, null=False)
    password = models.CharField(max_length=25, null=False)
    
    def __unicode__ (self):
        return self.role

class ServiceSpec (models.Model):
    """
    http_methods is a multi-valued field handled in the view by
    MultiValueField and MultiWidget
    """
    control_cluster = models.ForeignKey(ControlCluster)
    uri  = models.CharField(max_length=300, null=False)
    description = models.CharField(max_length=300, null=True)
    http_methods = models.CharField(max_length=20)
    
    def __unicode__ (self):
        return self.uri

class InputSpec (models.Model):
    """
    If the argument (here called input) has standard names such as:
    statType: port, queue, flow, aggregate, desc, table, features
    where name = 'statType' and
    values = 'port, queue, flow, aggregate, desc, table, features'
    Otherwise name = name and value  = 'regular expression'
    Example for name = switchid
    value = '^([0-9A-Fa-f]{1,2}[\.:-]){7}([0-9A-Fa-f]{1,2})$'
    """
    service_spec = models.ForeignKey(ServiceSpec)
    name = models.CharField(max_length=100, null=False)
    values = models.CharField(max_length=300, null=True)
    
    def __unicode__ (self):
        return self.name


class OutputSpec (models.Model):
    service_spec = models.ForeignKey(ServiceSpec)
    name = models.CharField(max_length=100, null=False)
    
    def __unicode__ (self):
        return self.name
