from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import TagDetailView, PostViewSet, PostCommentListView, PostTagListView, \
    CommentReplyListView, CommentDetailView, ReplyDetailView, ReplyAddsListView

router = SimpleRouter()
router.register('', PostViewSet)


urlpatterns = [
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),
    path('<int:pk>/comments/', PostCommentListView.as_view(), name='post-comment-list'),
    path('<int:pk>/tags/', PostTagListView.as_view(), name='post-tag-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:pk>/replies/', CommentReplyListView.as_view(), name='comment-reply-list'),
    path('comments/replies/<int:pk>/', ReplyDetailView.as_view(), name='reply-detail'),
    path('comments/replies/<int:pk>/adds/', ReplyAddsListView.as_view(), name='reply-adds-list'),
]

urlpatterns += router.urls
