from rest_framework import permissions

class IsOrderOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an order to perform actions.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request method is safe (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the order
        return obj.customer == request.user
