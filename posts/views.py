from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from .models import Tag, Post, Comment, Reply
from .serializers import TagSerializer, PostListSerializer, PostDetailSerializer, PostCommentListSerializer,\
    CommentDetailSerializer, CommentReplyListSerializer, ReplyDetailSerializer, ReplyAddsListSerializer
from .permissions import IsAuthorOrReadOnly
from .base_views import ReverseRelationListCreateView, get_from_kwargs
# Create your views here.


class TagDetailView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            return PostDetailSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentListView(ReverseRelationListCreateView):
    model_class = Post
    reverse_model_class = Comment
    serializer_class = PostCommentListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_perform_create_kwargs(self):
        kwargs = {'author': self.request.user, 'post': self.get_object()}
        return kwargs


class PostTagListView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        post = get_from_kwargs(self, Post)
        return post.tags.all()


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class CommentReplyListView(ReverseRelationListCreateView):
    model_class = Comment
    reverse_model_class = Reply
    reverse_field_related_name = 'replies'
    serializer_class = CommentReplyListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_perform_create_kwargs(self):
        kwargs = {'author': self.request.user, 'comment': self.get_object()}
        return kwargs


class ReplyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplyDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class ReplyAddsListView(ReverseRelationListCreateView):
    model_class = Reply
    reverse_field_related_name = 'adds'
    serializer_class = ReplyAddsListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_perform_create_kwargs(self):
        kwargs = {
            'author': self.request.user, 'comment': self.get_object().comment,
            'addsign': self.get_object()
        }
        return kwargs
