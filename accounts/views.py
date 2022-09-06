from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Post, Comment, Reply
from .permissions import IsAdminOrIsSelf, IsUserOrReadOnly, IsUserOrAdminReadOnly
from .base_views import UserReverseRelationListCreateView
from .throttling import CustomUserRateThrottle
from . import serializers, filters
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all().order_by('date_joined')
    throttle_classes = [CustomUserRateThrottle, ]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = filters.CustomUserFilterSet
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'last_name', 'date_joined']

    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            if self.request.version == '1.0':
                return serializers.CustomUserDetailSerializerVersion1
            elif self.request.version == '2.0':
                return serializers.CustomUserDetailSerializer
        return serializers.CustomUserListSerializer

    def get_permissions(self):
        permissions = []
        if self.kwargs.get('pk'):
            permissions.append(IsAdminOrIsSelf())
        else:
            permissions.append(IsAdminUser())
        return permissions


class UserPostListView(UserReverseRelationListCreateView):
    reverse_model_class = Post
    serializer_class = serializers.UserPostListSerializer
    permission_classes = [IsUserOrReadOnly, ]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'tags__title']
    ordering_fields = ['created_at', 'updated_at', 'status']
    filterset_class = filters.UserPostFilterSet

    def order_queryset(self, queryset):
        return queryset.order_by('-created_at')


class UserCommentListView(UserReverseRelationListCreateView):
    reverse_model_class = Comment
    serializer_class = serializers.UserCommentListSerializer
    permission_classes = [IsUserOrAdminReadOnly, ]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['post', 'commented_at', 'updated_at']
    filterset_class = filters.UserCommentFilterSet

    def order_queryset(self, queryset):
        return queryset.order_by('-commented_at')


class UserReplyListView(UserReverseRelationListCreateView):
    reverse_model_class = Reply
    reverse_field_related_name = 'replies'
    serializer_class = serializers.UserReplyListSerializer
    permission_classes = [IsUserOrAdminReadOnly, ]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['comment', 'replied_at', 'updated_at']
    filterset_class = filters.UserReplyFilterSet

    def order_queryset(self, queryset):
        return queryset.order_by('-replied_at')
