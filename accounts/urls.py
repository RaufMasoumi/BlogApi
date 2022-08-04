from django.urls import path
from rest_framework.routers import SimpleRouter
from posts.views import UserPostListView, UserCommentListView, UserReplyListView
from .views import UserViewSet

router = SimpleRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('posts/', UserPostListView.as_view(), name='user_post_list'),
    path('<int:pk>/posts/', UserPostListView.as_view(), name='user_post_list'),
    path('comments/', UserCommentListView.as_view(), name='user_comment_list'),
    path('<int:pk>/comments/', UserCommentListView.as_view(), name='user_comment_list'),
    path('replies/', UserReplyListView.as_view(), name='user_reply_list'),
    path('<int:pk>/replies/', UserReplyListView.as_view(), name='user_reply_list'),
]

urlpatterns += router.urls
