from rest_framework import serializers
from .models import Post, Comment, Reply


class PostsCountMixin:
    def get_posts_count(self, obj):
        return obj.posts.count()


class CommentsCountMixin:
    def get_comments_count(self, obj):
        return obj.comments.count()


class RepliesCountMixin:
    def get_replies_count(self, obj):
        return obj.replies.count()


class AddsCountMixin:
    def get_adds_count(self, obj):
        return obj.adds.count()


class CommentNestedSerializer(serializers.HyperlinkedModelSerializer, RepliesCountMixin):
    author = serializers.StringRelatedField()
    short_comment = serializers.CharField(read_only=True, max_length=150, source='make_short_comment')
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['url', 'author', 'short_comment', 'replies_count']


class PostNestedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['url', 'title']


class ReplyNestedSerializer(serializers.HyperlinkedModelSerializer, AddsCountMixin):
    author = serializers.StringRelatedField()
    short_reply = serializers.CharField(source='make_short_reply')
    adds_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['url', 'author', 'short_reply', 'adds_count']


class AddsignNestedSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField()
    short_reply = serializers.CharField(source='make_short_reply')

    class Meta:
        model = Reply
        fields = ['url', 'author', 'short_reply']
