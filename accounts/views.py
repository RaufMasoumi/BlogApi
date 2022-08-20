from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser
from posts.models import Post, Comment, Reply
from .serializers import CustomUserListSerializer, CustomUserDetailSerializer, UserPostListSerializer, \
    UserCommentListSerializer, UserReplyListSerializer
from .permissions import IsAdminOrUser, IsUserOrReadOnly, IsUserOrAdminReadOnly
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            return CustomUserDetailSerializer
        return CustomUserListSerializer

    def get_permissions(self):
        permissions = []
        if self.kwargs.get('pk'):
            permissions.append(IsAdminOrUser())
        else:
            permissions.append(IsAdminUser())
        return permissions


class UserReverseRelationListCreateView(ListCreateAPIView):
    serializer_class_pattern = 'User_RelatedClass_ListSerializer'
    reverse_model_class = None
    reverse_model_user_field_name = 'author'
    reverse_field_related_name = None

    def get_reverse_field_related_name(self):
        if self.reverse_field_related_name:
            return self.reverse_field_related_name
        lower_model_class_name = self.reverse_model_class.__name__.lower()
        return lower_model_class_name + 's'

    def get_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        model_class_name = self.reverse_model_class.__name__
        serializer_class_name = self.serializer_class_pattern.replace(
            '_RelatedClass_', model_class_name
        )
        exec(f'serializer_class = {serializer_class_name}')
        return locals().get('serializer_class')

    def get_user_obj(self):
        return get_user(self, or_from_request=True)

    def get_queryset(self):
        user = self.get_user_obj()
        queryset = getattr(user, self.get_reverse_field_related_name())
        return queryset.all()

    def perform_create(self, serializer):
        kwargs = {self.reverse_model_user_field_name: self.get_user_obj()}
        serializer.save(**kwargs)


class UserPostListView(UserReverseRelationListCreateView):
    reverse_model_class = Post
    permission_classes = [IsUserOrReadOnly, ]


class UserCommentListView(UserReverseRelationListCreateView):
    reverse_model_class = Comment
    permission_classes = [IsUserOrAdminReadOnly, ]


class UserReplyListView(UserReverseRelationListCreateView):
    reverse_model_class = Reply
    reverse_field_related_name = 'replies'
    permission_classes = [IsUserOrAdminReadOnly, ]


def get_user(view_obj, or_from_request=False):
    user_pk = None
    if view_obj.kwargs.get('pk'):
        user_pk = view_obj.kwargs['pk']

    elif or_from_request and view_obj.request.user.is_authenticated:
        user_pk = view_obj.request.user.pk

    return get_object_or_404(get_user_model(), pk=user_pk)
