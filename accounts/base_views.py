from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from posts.base_views import ReverseRelationListCreateView


class UserReverseRelationListCreateView(ReverseRelationListCreateView):

    def get_object(self):
        return get_user(self, or_from_request=True)

    def get_perform_create_kwargs(self):
        kwargs = {'author': self.request.user}
        return kwargs


def get_user(view_obj, or_from_request=False):
    user_slug = None
    if view_obj.kwargs.get('slug'):
        user_slug = view_obj.kwargs['slug']

    elif or_from_request and view_obj.request.user.is_authenticated:
        user_slug = view_obj.request.user.slug

    return get_object_or_404(get_user_model(), slug=user_slug)
