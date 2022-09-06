from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView


class ReverseRelationListCreateView(ListCreateAPIView):
    model_class = None
    reverse_model_class = None
    reverse_field_related_name = None

    def get_reverse_field_related_name(self):
        if self.reverse_field_related_name:
            return self.reverse_field_related_name
        lower_model_class_name = self.reverse_model_class.__name__.lower()
        return f'{lower_model_class_name}s'

    def get_object(self):
        return get_from_kwargs(self, self.model_class)

    def get_queryset(self):
        obj = self.get_object()
        queryset = getattr(obj, self.get_reverse_field_related_name())
        return queryset.all()

    def get_perform_create_kwargs(self) -> dict:
        return {}

    def perform_create(self, serializer):
        kwargs = self.get_perform_create_kwargs()
        if kwargs:
            serializer.save(**kwargs)


def get_from_kwargs(view_obj, get_class):
    pk = view_obj.kwargs.get('pk')
    return get_object_or_404(get_class, pk=pk)
