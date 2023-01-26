from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from posts.models import Post


class ReverseRelationListCreateView(ListCreateAPIView):
    parent_klass = None
    reverse_model_class = None
    reverse_field_related_name = None

    def get_reverse_field_related_name(self):
        if self.reverse_field_related_name:
            return self.reverse_field_related_name
        lower_model_class_name = self.reverse_model_class.__name__.lower()
        return f'{lower_model_class_name}s'

    def get_object(self):
        return get_from_kwargs(self.kwargs, self.parent_klass)

    def get_queryset(self):
        obj = self.get_object()
        queryset = getattr(obj, self.get_reverse_field_related_name())
        queryset = self.order_queryset(queryset)
        return queryset.all()

    def order_queryset(self, queryset):
        return queryset.order_by('id')

    def get_perform_create_kwargs(self) -> dict:
        return {}

    def perform_create(self, serializer):
        kwargs = self.get_perform_create_kwargs()
        if kwargs:
            serializer.save(**kwargs)


def make_post_queryset_for_user(request):
    if request.user.is_staff:
        return Post.objects.all()
    else:
        published_queryset = Post.objects.published()
        if request.user.is_authenticated:
            draft_queryset = Post.objects.user_draft(request.user)
            return published_queryset | draft_queryset

        return published_queryset


def get_from_kwargs(lookup_dict, get_klass):
    pk = lookup_dict.get('pk')
    return get_object_or_404(get_klass, pk=pk)
