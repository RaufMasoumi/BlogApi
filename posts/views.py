from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from accounts.views import get_user
from .models import Tag, Post, Comment, Reply
from .serializers import TagSerializer, PostListSerializer, PostDetailSerializer, PostCommentListSerializer,\
    CommentDetailSerializer, CommentReplyListSerializer, ReplyDetailSerializer, ReplyAddsListSerializer
from .permissions import IsAuthorOrReadOnly
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


class PostCommentListView(ListCreateAPIView):
    serializer_class = PostCommentListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_post_obj(self):
        return get_from_kwargs(self, Post)

    def get_queryset(self):
        post = self.get_post_obj()
        return post.comments.all()

    def perform_create(self, serializer):
        user = get_user(self, or_from_request=True)
        serializer.save(author=user, post=self.get_post_obj())


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


class CommentReplyListView(ListCreateAPIView):
    serializer_class = CommentReplyListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_comment_obj(self):
        return get_from_kwargs(self, Comment)

    def get_queryset(self):
        comment = self.get_comment_obj()
        return comment.replies.all()

    def perform_create(self, serializer):
        user = get_user(self, or_from_request=True)
        serializer.save(author=user, comment=self.get_comment_obj())


class ReplyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplyDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class ReplyAddsListView(ListCreateAPIView):
    serializer_class = ReplyAddsListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_reply_obj(self):
        return get_from_kwargs(self, Reply)

    def get_queryset(self):
        reply = self.get_reply_obj()
        return reply.adds.all()

    def perform_create(self, serializer):
        user = get_user(self, or_from_request=True)
        reply = self.get_reply_obj()
        serializer.save(author=user, comment=reply.comment, addsign=reply)


def get_from_kwargs(view_obj, get_class):
    pk = view_obj.kwargs.get('pk')
    return get_object_or_404(get_class, pk=pk)
