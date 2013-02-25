from provinet.core.memberships.models import Membership
from django.contrib.auth.models import Group


def getProjectOwner(pj):
    """
    Return the user owner of the project
    """
    mb = Membership.objects.get(project=pj, group=Group.objects.get(id=1))
    return mb.user 