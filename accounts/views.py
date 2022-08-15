from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from posts.permissions import IsAuthorOrReadOnly
from .serializers import CustomUserSerializer, UserPostListSerializer, UserCommentListSerializer, \
    UserReplyListSerializer
from .permissions import IsAdminOrAuthor
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser, ]


class UserPostListView(ListCreateAPIView):
    serializer_class = UserPostListSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_user_obj(self):
        return get_user(self, or_from_request=True)

    def get_queryset(self):
        user = self.get_user_obj()
        return user.posts.all()

    def perform_create(self, serializer):
        serializer.save(author=self.get_user_obj())


class UserCommentListView(ListCreateAPIView):
    serializer_class = UserCommentListSerializer
    permission_classes = [IsAdminOrAuthor, ]

    def get_user_obj(self):
        return get_user(self, or_from_request=True)

    def get_queryset(self):
        user = self.get_user_obj()
        return user.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.get_user_obj())


class UserReplyListView(ListCreateAPIView):
    serializer_class = UserReplyListSerializer
    permission_classes = [IsAdminOrAuthor, ]

    def get_user_obj(self):
        return get_user(self, or_from_request=True)

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

