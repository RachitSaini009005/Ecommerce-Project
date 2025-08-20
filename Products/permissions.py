from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwnerOrReadOnly(BasePermission):  # when you inherit from BasePermission,you're telling Django Rest framework: "This class defines permission rules that DRF should enforce on views or viewsets"
    def has_permission(self, request, view):
        # Everyone can read (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Anyone logged in can create (POST)
        if request.method == "POST":
            return request.user and request.user.is_authenticated
        # For PUT/PATCH/DELETE we also need to be authenticated (object check below)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read is OK for everyone
        if request.method in SAFE_METHODS:
            return True
        # Write only if admin OR the creator of this product
        return (request.user and request.user.is_staff) or (obj.owner_id == request.user.id)
        # this measn if user is logged in and isa staff/admin      If th user is the owner of the object  