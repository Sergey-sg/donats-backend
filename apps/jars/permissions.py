from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from ..user.models import VolunteerInfo


class JarPermission(BasePermission):
    """
    Custom permission class for Jar API views.

    Allows POST requests only for active volunteers.
    Allows GET requests for all users.
    """
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.

        Returns True for GET requests.
        Returns True only if the volunteer is active for POST requests.
        Returns False otherwise.
        """
        if request.method == 'POST' or request.method == 'DELETE':
            try:
                volunteer = VolunteerInfo.objects.get(user=request.user.pk)
                return volunteer.active
            except ObjectDoesNotExist:
                return False

        if request.method == 'GET':
            return True
