from rest_framework import serializers
from .models import Post, Comment, Reply


class CommentNestedSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField()
    short_comment = serializers.CharField(read_only=True, max_length=150, source='make_short_comment')
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['url', 'author', 'short_comment', 'replies_count']

    def get_replies_count(self, obj):
        return obj.replies.count()


class PostNestedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['url', 'title']


class ReplyNestedSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField()
    short_reply = serializers.CharField(source='make_short_reply')
    adds_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['url', 'author', 'short_reply', 'adds_count']

    def get_adds_count(self, obj):
        return obj.adds.count()
