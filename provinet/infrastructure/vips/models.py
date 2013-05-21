from django.db import models

class VIP (models.Model):
    METHODS = (
           ('post','POST'),
           ('put','PUT'),
           ('get','GET')
           )
    
    PROTOCOLS = (
           ('https','HTTPS'),
           ('http','HTTP'),
           ('ssh','SSH')
           )
    
    name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=50, null=False)
    uri = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=700)
    protocol = models.CharField(max_length=5,choices=PROTOCOLS, null=False)
    method = models.CharField(max_length=5,choices=METHODS, null=False)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __unicode__ (self):
        return self.name
