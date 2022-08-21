from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from posts.models import Post, Comment, Reply
from .serializers import CustomUserListSerializer, CustomUserDetailSerializer, UserPostListSerializer, \
    UserCommentListSerializer, UserReplyListSerializer
from .permissions import IsAdminOrUser, IsUserOrReadOnly, IsUserOrAdminReadOnly
from .base_views import UserReverseRelationListCreateView
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


class UserPostListView(UserReverseRelationListCreateView):
    reverse_model_class = Post
    serializer_class = UserPostListSerializer
    permission_classes = [IsUserOrReadOnly, ]


class UserCommentListView(UserReverseRelationListCreateView):
    reverse_model_class = Comment
    serializer_class = UserCommentListSerializer
    permission_classes = [IsUserOrAdminReadOnly, ]


class UserReplyListView(UserReverseRelationListCreateView):
    reverse_model_class = Reply
    reverse_field_related_name = 'replies'
    serializer_class = UserReplyListSerializer
    permission_classes = [IsUserOrAdminReadOnly, ]
