from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Post, Comment, Reply
from .serializers import TagSerializer, PostSerializer, CommentSerializer, ReplySerializer
from .permissions import IsAuthorOrReadOnly
# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class PostCommentListView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        return post.comments.all()


class PostTagListView(ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        return post.tags.all()


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class CommentReplyListView(ListCreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        comment_pk = self.kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        return comment.replies.all()


class ReplyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthorOrReadOnly, ]


class ReplyAddsListView(ListCreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        reply_pk = self.kwargs.get('pk')
        reply = get_object_or_404(Reply, pk=reply_pk)
        return reply.adds.all()
