from rest_framework.permissions import BasePermission
from posts.permissions import is_request_safe_method


class IsSelfOrAdmin(BasePermission):
    """
        Checks that the requested user is the view object or the user is an Admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj == request.user:
            return True

        return False


class IsSelfOrReadOnly(BasePermission):
    """
        Checks that if the requested user is the view object or the request is safe.
    """
    def has_permission(self, request, view):
        if is_request_safe_method(request) or view.get_object() == request.user:
            return True

        return False


class IsSelfOrAdminReadOnly(BasePermission):
    """
        Checks that if the requested user is the view object or
        the request is safe and the requested user is an Admin.
    """
    def has_permission(self, request, view):
        if is_request_safe_method(request) and request.user.is_staff:
            return True

        elif view.get_object() == request.user:
            return True

        return False
