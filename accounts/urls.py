from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, UserPostListView, UserCommentListView, UserReplyListView

router = SimpleRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('posts/', UserPostListView.as_view(), name='user-post-list'),
    path('<int:pk>/posts/', UserPostListView.as_view(), name='user-post-list'),
    path('comments/', UserCommentListView.as_view(), name='user-comment-list'),
    path('<int:pk>/comments/', UserCommentListView.as_view(), name='user-comment-list'),
    path('replies/', UserReplyListView.as_view(), name='user-reply-list'),
    path('<int:pk>/replies/', UserReplyListView.as_view(), name='user-reply-list'),
]

urlpatterns += router.urls
