from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Tag, Post, Comment, Reply
from posts.nested_serializers import PostNestedSerializer, CommentNestedSerializer, AddsignNestedSerializer, \
    PostsCountMixin, CommentsCountMixin, RepliesCountMixin, AddsCountMixin


class CustomUserListSerializer(serializers.ModelSerializer, PostsCountMixin, CommentsCountMixin):
    profile = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='slug')
    password_confirm = serializers.CharField(write_only=True, help_text='Required. should be same as password')
    posts_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'profile', 'username', 'password', 'password_confirm', 'email', 'first_name', 'last_name',
            'posts_count', 'comments_count',
        ]
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
        instance = get_user_model().objects.create_user(**validated_data)
        return instance


class CustomUserDetailSerializerVersion1(serializers.ModelSerializer, CommentsCountMixin):
    profile = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='slug')
    password = serializers.CharField(read_only=True, source='get_safe_password')
    posts = PostNestedSerializer(read_only=True, many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['profile', 'username', 'password', 'email', 'first_name', 'last_name',
                  'date_joined', 'posts', 'comments_count']
        extra_kwargs = {
            'date_joined': {'read_only': True}
        }


class CustomUserDetailSerializer(serializers.ModelSerializer, CommentsCountMixin):
    profile = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='slug')
    password = serializers.CharField(read_only=True, source='get_safe_password')
    posts = PostNestedSerializer(read_only=True, many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['profile', 'username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'slug',
                  'date_joined', 'posts', 'comments_count']
        extra_kwargs = {
            'date_joined': {'read_only': True}
        }


class UserPostListSerializer(serializers.HyperlinkedModelSerializer, CommentsCountMixin):
    short_description = serializers.CharField(read_only=True, source='make_short_description')
    comments_count = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(slug_field='tag', queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'url', 'title', 'thumbnail', 'description', 'short_description',
            'tags', 'comments_count', 'status',
        ]
        extra_kwargs = {
            'description': {'write_only': True, 'required': False},
            'status': {'read_only': True},
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
