from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag, Post, Comment, Reply
from .permissions import IsAuthorOrReadOnly
from .base_views import ReverseRelationListCreateView, get_from_kwargs
from .filters import PostFilterSet, CommentFilterSet, ReplyFilterSet
from . import serializers
# Create your views here.


class TagDetailView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'author__username', 'tags__title']
    ordering_fields = ['author', 'created_at', 'updated_at', 'status']
    filterset_class = PostFilterSet

    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            return serializers.PostDetailSerializer
        return serializers.PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentListView(ReverseRelationListCreateView):
    model_class = Post
    reverse_model_class = Comment
    serializer_class = serializers.PostCommentListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['author', 'commented_at', 'updated_at']
    filterset_class = CommentFilterSet

    def get_perform_create_kwargs(self):
        kwargs = {'author': self.request.user, 'post': self.get_object()}
        return kwargs


class PostTagListView(ListAPIView):
    serializer_class = serializers.TagSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        post = get_from_kwargs(self, Post)
        return post.tags.all()


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class CommentReplyListView(ReverseRelationListCreateView):
    model_class = Comment
    reverse_model_class = Reply
    reverse_field_related_name = 'replies'
    serializer_class = serializers.CommentReplyListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['author', 'replied_at', 'updated_at']
    filterset_class = ReplyFilterSet

    def get_perform_create_kwargs(self):
        kwargs = {'author': self.request.user, 'comment': self.get_object()}
        return kwargs


class ReplyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = serializers.ReplyDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class ReplyAddsListView(ReverseRelationListCreateView):
    model_class = Reply
    reverse_field_related_name = 'adds'
    serializer_class = serializers.ReplyAddsListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['author', 'replied_at', 'updated_at']
    filterset_class = ReplyFilterSet

    def get_perform_create_kwargs(self):
        kwargs = {
            'author': self.request.user, 'comment': self.get_object().comment,
            'addsign': self.get_object()
        }
        return kwargs
