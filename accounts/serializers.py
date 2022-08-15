from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Tag, Post, Comment, Reply
from posts.nested_serializers import PostNestedSerializer, CommentNestedSerializer, ReplyNestedSerializer


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'url', 'username', 'email', 'first_name', 'last_name', 'posts_count', 'comments_count'
        ]
        extra_kwargs = {
            'url': {'view_name': 'user-detail'},
        }

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class UserPostListSerializer(serializers.HyperlinkedModelSerializer):
    short_description = serializers.CharField(read_only=True, source='make_short_description')
    comments_count = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(slug_field='title', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Post
        fields = [
            'url', 'title', 'thumbnail', 'description', 'short_description',
            'tags', 'comments_count', 'status',
        ]
        extra_kwargs = {
            'description': {'write_only': True, },
        }

    def get_comments_count(self, obj):
        return obj.comments.count()


class UserCommentListSerializer(serializers.HyperlinkedModelSerializer):
    post_detail = PostNestedSerializer(read_only=True, source='post')
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'url', 'post', 'post_detail', 'comment', 'replies_count', 'commented_at', 'updated_at',
        ]
        extra_kwargs = {
            'post': {'write_only': True},
        }

    def get_replies_count(self, obj):
        return obj.replies.count()


class UserReplyListSerializer(serializers.HyperlinkedModelSerializer):
    comment_detail = CommentNestedSerializer(read_only=True, source='comment')
    addsign_detail = ReplyNestedSerializer(read_only=True, source='addsign')
    adds_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'url', 'comment', 'comment_detail', 'addsign', 'addsign_detail', 'reply',
            'adds_count', 'replied_at', 'updated_at',
        ]
        extra_kwargs = {
            'comment': {'write_only': True},
            'addsign': {'write_only': True},
        }

    def get_adds_count(self, obj):
        return obj.adds.count()


def get_user_from_context(serializer_obj):
    request = serializer_obj.context.get('request')
    return request.user if request.user.is_authenticated else None
