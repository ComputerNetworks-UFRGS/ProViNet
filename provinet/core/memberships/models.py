from django.db import models
from django.contrib.auth.models import User,Group
from provinet.core.projects.models import Project

class Membership (models.Model):
    """
    Using User and Group from django.contrib.auth.models
    """
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    project = models.ForeignKey(Project)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__ (self):
        return "Member"
