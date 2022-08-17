from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS


class IsAdminOrUser(BasePermission):
    """
        Checks that the requested user is the same user of the view or the user is an Admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.user == obj:
            return True

        return False


class IsUserOrReadOnly(BasePermission):
    """
        Checks that if the methods are safe or the requested user is the same user of the view.
    """
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        elif request.user == view.get_user_obj():
            return True

        return False


class IsUserOrAdminReadOnly(BasePermission):
    """
        Checks that if the methods are safe and the user is an Admin
        or the requested user is the same user of the view.
    """
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS and request.user.is_staff:
            return True
        elif request.user == view.get_user_obj():
            return True

        return False
