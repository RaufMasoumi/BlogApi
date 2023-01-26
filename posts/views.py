from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag, Post, Comment, Reply
from .permissions import IsAuthorOrReadOnly
from .base_views import ReverseRelationListCreateView, get_from_kwargs, make_post_queryset_for_user
from .filters import PostFilterSet, CommentFilterSet, ReplyFilterSet
from . import serializers
# Create your views here.


class TagDetailView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [AllowAny, ]


class PostListCreateView(ListCreateAPIView):
    serializer_class = serializers.PostListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'author__username', 'tags__title']
    ordering_fields = ['author', 'created_at', 'updated_at']
    filterset_class = PostFilterSet

    def get_queryset(self):
        return make_post_queryset_for_user(self.request).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_serializer_class(self):
        if self.get_object().is_published():
            return serializers.PostDetailSerializer
        else:
            return serializers.DraftPostDetailSerializer

    def get_queryset(self):
        return make_post_queryset_for_user(self.request)


class PostCommentListView(ReverseRelationListCreateView):
    parent_klass = Post.objects.published()
    reverse_model_class = Comment
    serializer_class = serializers.PostCommentListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['author', 'commented_at', 'updated_at']
    filterset_class = CommentFilterSet

    def get_perform_create_kwargs(self):
        kwargs = {'author': self.request.user, 'post': self.get_object()}
        return kwargs

    def order_queryset(self, queryset):
        return queryset.order_by('-commented_at')


class PostTagListView(ListAPIView):
    serializer_class = serializers.TagSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        post = get_from_kwargs(self.kwargs, Post)
        return post.tags.order_by('title')


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class CommentReplyListView(ReverseRelationListCreateView):
    parent_klass = Comment
    reverse_field_related_name = 'replies'
    serializer_class = serializers.CommentReplyListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['author', 'replied_at', 'updated_at']
    filterset_class = ReplyFilterSet

    def get_perform_create_kwargs(self):
        kwargs = {'author': self.request.user, 'comment': self.get_object()}
        return kwargs

    def order_queryset(self, queryset):
        return queryset.order_by('-replied_at')


class ReplyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = serializers.ReplyDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class ReplyAddsListView(ReverseRelationListCreateView):
    parent_klass = Reply
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

    def order_queryset(self, queryset):
        return queryset.order_by('-replied_at')
