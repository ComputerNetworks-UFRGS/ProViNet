from django.db import models
from django.contrib.auth.models import User

class Project (models.Model):
    name = models.CharField(max_length=50, null=False)
    members = models.ManyToManyField(User, through='memberships.Membership', blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def getOwner(self):
        return self.membership_set.get(group_id=1).user

    def __unicode__ (self):
        return self.name