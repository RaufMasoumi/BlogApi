from rest_framework import serializers
from accounts.nested_serializers import CustomUserNestedSerializer
from .models import Tag, Post, Comment, Reply
from . import nested_serializers


class PostListSerializer(serializers.HyperlinkedModelSerializer, nested_serializers.CommentsCountMixin):
    author = serializers.StringRelatedField()
    short_description = serializers.CharField(read_only=True, source='make_short_description')
    comments_count = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(slug_field='title', queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'url', 'title', 'author', 'thumbnail', 'description', 'short_description',
            'tags', 'comments_count', 'status',
        ]
        extra_kwargs = {
            'description': {'write_only': True, 'required': False},
        }


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserNestedSerializer(read_only=True)
    tags = serializers.SlugRelatedField(slug_field='title', queryset=Tag.objects.all(), many=True, required=False)
    comments = nested_serializers.CommentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'url', 'title', 'author', 'thumbnail', 'description', 'comments',
            'tags', 'created_at', 'updated_at', 'status',
        ]
        extra_kwargs = {
            'description': {'required': False}
        }


class PostCommentListSerializer(serializers.HyperlinkedModelSerializer, nested_serializers.RepliesCountMixin):
    author = CustomUserNestedSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'url', 'author', 'comment', 'replies_count', 'commented_at', 'updated_at',
        ]


class TagSerializer(serializers.ModelSerializer):
    posts = PostListSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['title', 'posts']


class CommentDetailSerializer(serializers.HyperlinkedModelSerializer):
    post = nested_serializers.PostNestedSerializer(read_only=True)
    author = CustomUserNestedSerializer(read_only=True)
    replies = nested_serializers.ReplyNestedSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ['url', 'post', 'author', 'comment', 'replies', 'commented_at', 'updated_at']


class CommentReplyListSerializer(serializers.HyperlinkedModelSerializer, nested_serializers.AddsCountMixin):
    author = CustomUserNestedSerializer(read_only=True)
    addsign_detail = nested_serializers.AddsignNestedSerializer(read_only=True, source='addsign')
    adds_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'url', 'author', 'addsign', 'addsign_detail', 'reply', 'adds_count',
            'replied_at', 'updated_at',
        ]
        extra_kwargs = {
            'addsign': {'write_only': True},
        }


class ReplyDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserNestedSerializer(read_only=True)
    addsign = nested_serializers.ReplyNestedSerializer(read_only=True)
    adds = nested_serializers.ReplyNestedSerializer(read_only=True, many=True)

    class Meta:
        model = Reply
        fields = [
            'url', 'author', 'comment', 'addsign', 'reply', 'adds', 'replied_at', 'updated_at'
        ]
        extra_kwargs = {
            'comment': {'read_only': True, }
        }


class ReplyAddsListSerializer(serializers.HyperlinkedModelSerializer, nested_serializers.AddsCountMixin):
    author = CustomUserNestedSerializer(read_only=True)
    adds_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'url', 'author', 'reply', 'adds_count', 'replied_at', 'updated_at',
        ]
