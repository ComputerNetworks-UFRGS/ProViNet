from django.db import models
from provinet.development.modules.models import Module

"""
The classes below are used to map WADL resources. More
information at: http://www.w3.org/Submission/wadl/
"""

class Service (models.Model):
    module = models.ForeignKey(Module)
    path = models.CharField(max_length=1024, null=False)
    description = models.CharField(max_length=1024)
    
    def __unicode__ (self):
        return self.path


class Method (models.Model):
    METHODS = (
               ('post', 'POST'),
               ('get', 'GET'),
               ('put', 'PUT'),
               ('delete', 'DELETE'),
               )
    
    service = models.ForeignKey(Service)
    method_id = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=6, choices=METHODS, null=False)
    
    def __unicode__ (self):
        return self.name
    
class Param (models.Model):
    STYLES = (
           ('matrix', 'Matrix'),
           ('header', 'Header'),
           ('query', 'Query'),
           ('template', 'Template'),
           ('plain', 'Plain'),
           )

    method = models.ForeignKey(Method, null=True)
    service = models.ForeignKey(Service, null=True)
    name = models.CharField(max_length=256, null=False)
    style = models.CharField(max_length=8, choices=STYLES)
    type = models.CharField(max_length=256, null=True)
    is_required = models.BooleanField()
    # Multi Valued field handled in the view with ";" as split parameter
    values = models.CharField(max_length=1024, null=True)

    def __unicode__ (self):
        return self.name
    
class Response (models.Model):
    method = models.ForeignKey(Method)
    name = models.CharField(max_length=256, null=False)
    value = models.TextField()
    
    def __unicode__ (self):
        return self.name
    
