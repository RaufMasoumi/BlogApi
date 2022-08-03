from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, PostCommentListView, PostTagListView, CommentReplyListView, CommentDetailView, \
        ReplyDetailView, ReplyAddsListView

router = SimpleRouter()
router.register('', PostViewSet)

urlpatterns = [
    path('<int:pk>/comments/', PostCommentListView.as_view(), name='post_comment_list'),
    path('<int:pk>/tags/', PostTagListView.as_view(), name='post_tag_list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comments/<int:pk>/replies/', CommentReplyListView.as_view(), name='comment_reply_list'),
    path('replies/<int:pk>/', ReplyDetailView.as_view(), name='reply_detail'),
    path('replies/<int:pk>/adds/', ReplyAddsListView.as_view(), name='reply_adds_list'),
]

urlpatterns += router.urls
