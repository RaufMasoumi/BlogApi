from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_request_safe_method(request):
    return True if request.method in SAFE_METHODS else False


class IsAuthenticatedOrReadOnly(BasePermission):
    """
        Checks that if the requested user is authenticated or the request is safe.
    """
    def has_permission(self, request, view):
        if is_request_safe_method(request) or request.user.is_authenticated:
            return True

        return False


class IsAuthorOrReadOnly(BasePermission):
    """
        Checks that if the requested user is the author of the object or the request is safe.
    """
    def has_object_permission(self, request, view, obj):
        if is_request_safe_method(request):
            return True

        elif getattr(obj, 'author', None) and obj.author == request.user:
            return True

        return False
