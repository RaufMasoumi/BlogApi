from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser


class IsAdminOrAuthor(IsAdminUser):
    """
        Checks that if the view has been called with user pk,
        the user is the author of the list(collection) or the user is an Admin.
    """
    def has_permission(self, request, view):
        user_pk = view.kwargs.get('pk')
        if user_pk:
            user = get_user_model().objects.get(pk=user_pk)
            if user == request.user:
                return True

        return super().has_permission(request, view)
