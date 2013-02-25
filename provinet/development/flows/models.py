from django.db import models
from provinet.development.services.models import Service


class Wildcard (models.Model):
    ingress_port = models.IntegerField()
    src_mac = models.CharField(max_length=17)
    dst_mac = models.CharField(max_length=17)
    vlan_id = models.CharField(max_length=200)
    vlan_priority = models.CharField(max_length=20)
    ether_type = models.CharField(max_length=200)
    tos_bits = models.IntegerField()
    protocol = models.CharField(max_length=200)
    src_ip = models.CharField(max_length=15)
    dst_ip = models.CharField(max_length=15)
    src_port = models.IntegerField()
    dst_port = models.IntegerField()
    
    def __unicode__ (self):
        return "wildcard"
    
class Flow (models.Model):
    """
    This model represents an OpenFlow 1.0 Flow
    """
    
    service = models.ForeignKey(Service)
    name = models.CharField(max_length=200)
    switchid = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    wildcard = models.ForeignKey(Wildcard)
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __unicode__ (self):
        return self.name

class Action (models.Model):
    """
    'output' possible values = <number>, all, controller, local, ingress-port, normal, flood 
    """
    
    flow = models.ForeignKey(Flow)
    output = models.IntegerField()
    enqueue = models.CharField(max_length=200)
    set_vlan_id = models.CharField(max_length=200)
    set_vlan_priority = models.CharField(max_length=200)
    set_src_mac = models.CharField(max_length=17)
    set_dst_mac = models.CharField(max_length=17)
    set_tos_bits = models.IntegerField()
    set_src_ip = models.CharField(max_length=15)
    set_dst_ip = models.CharField(max_length=15)
    set_src_port = models.CharField(max_length=20)
    set_dst_port = models.CharField(max_length=20)
    
    def __unicode__ (self):
        return "Action"
    