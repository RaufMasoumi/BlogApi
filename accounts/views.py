from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser
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


class GetUserObjMixin:
    request = None
    kwargs = None

    def get_user_obj(self):
        return get_user(self, or_from_request=True)


class UserPostListView(ListCreateAPIView, GetUserObjMixin):
    serializer_class = UserPostListSerializer
    permission_classes = [IsUserOrReadOnly, ]

    def get_queryset(self):
        user = self.get_user_obj()
        return user.posts.all()

    def perform_create(self, serializer):
        serializer.save(author=self.get_user_obj())


class UserCommentListView(ListCreateAPIView, GetUserObjMixin):
    serializer_class = UserCommentListSerializer
    permission_classes = [IsUserOrAdminReadOnly, ]

    def get_queryset(self):
        user = self.get_user_obj()
        return user.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.get_user_obj())


class UserReplyListView(ListCreateAPIView, GetUserObjMixin):
    serializer_class = UserReplyListSerializer
    permission_classes = [IsUserOrAdminReadOnly, ]

    def get_queryset(self):
        user = self.get_user_obj()
        return user.replies.all()

    def perform_create(self, serializer):
        serializer.save(author=self.get_user_obj())


def get_user(view_obj, or_from_request=False):
    user_pk = None
    if view_obj.kwargs.get('pk'):
        user_pk = view_obj.kwargs['pk']

    elif or_from_request and view_obj.request.user.is_authenticated:
        user_pk = view_obj.request.user.pk

    return get_object_or_404(get_user_model(), pk=user_pk)
