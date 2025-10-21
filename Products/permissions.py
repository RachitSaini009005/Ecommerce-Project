# Products/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Custom permission:
    - SAFE_METHODS (GET, HEAD, OPTIONS): Allow for everyone
    - POST: Allow only authenticated users
    - PUT/PATCH/DELETE: Allow only product owner or staff admin
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for anyone
        if request.method in SAFE_METHODS:
            return True
        # For other requests, user must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE methods always allowed
        if request.method in SAFE_METHODS:
            return True
        # Only owner or admin can update/delete
        return obj.owner == request.user or request.user.is_staff
