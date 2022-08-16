from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Tag, Post, Comment, Reply
from posts.nested_serializers import PostNestedSerializer, CommentNestedSerializer, AddsignNestedSerializer, \
    PostsCountMixin, CommentsCountMixin, RepliesCountMixin, AddsCountMixin


class CustomUserListSerializer(serializers.ModelSerializer, PostsCountMixin, CommentsCountMixin):
    profile = serializers.HyperlinkedIdentityField(view_name='user-detail')
    password_confirm = serializers.CharField(write_only=True, help_text='Required. should be same as password')
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'profile', 'username', 'password', 'password_confirm', 'email', 'first_name', 'last_name',
            'posts_count', 'comments_count',
        ]
        read_only_fields = ['email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password_confirm(self, value):
        password = self.initial_data.get('password')
        if not value == password:
            message = 'Password confirmation failed! Enter the same password to confirm.'
            raise serializers.ValidationError(message)
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return super().create(validated_data)


class CustomUserDetailSerializer(serializers.ModelSerializer, CommentsCountMixin):
    profile = serializers.HyperlinkedIdentityField(view_name='user-detail')
    password = serializers.CharField(source='get_safe_password', read_only=True)
    posts = PostNestedSerializer(read_only=True, many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['profile', 'username', 'password', 'email', 'first_name', 'last_name',
                  'date_joined', 'posts', 'comments_count']
        extra_kwargs = {
            'date_joined': {'read_only': True}
        }


class UserPostListSerializer(serializers.HyperlinkedModelSerializer, CommentsCountMixin):
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


class UserCommentListSerializer(serializers.HyperlinkedModelSerializer, RepliesCountMixin):
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


class UserReplyListSerializer(serializers.HyperlinkedModelSerializer, AddsCountMixin):
    comment_detail = CommentNestedSerializer(read_only=True, source='comment')
    addsign_detail = AddsignNestedSerializer(read_only=True, source='addsign')
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
