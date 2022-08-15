from rest_framework import serializers
from accounts.nested_serializers import CustomUserNestedSerializer
from .nested_serializers import CommentNestedSerializer, PostNestedSerializer, ReplyNestedSerializer
from .models import Tag, Post, Comment, Reply


class PostListSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField()
    short_description = serializers.CharField(read_only=True, source='make_short_description')
    comments_count = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(slug_field='title', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Post
        fields = [
            'url', 'title', 'author', 'thumbnail', 'description', 'short_description',
            'tags', 'comments_count', 'status',
        ]
        extra_kwargs = {
            'description': {'write_only': True, },
        }

    def get_comments_count(self, obj):
        return obj.comments.count()


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserNestedSerializer(read_only=True)
    tags = serializers.SlugRelatedField(slug_field='title', queryset=Tag.objects.all(), many=True)
    comments = CommentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'url', 'title', 'author', 'thumbnail', 'description', 'comments',
            'tags', 'created_at', 'updated_at', 'status',
        ]


class PostCommentListSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserNestedSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'url', 'author', 'comment', 'replies_count', 'commented_at', 'updated_at',
        ]

    def get_replies_count(self, obj):
        return obj.replies.count()


class TagSerializer(serializers.ModelSerializer):
    posts = PostListSerializer(many=True)

    class Meta:
        model = Tag
        fields = ['title', 'posts']


class CommentDetailSerializer(serializers.HyperlinkedModelSerializer):
    post = PostNestedSerializer(read_only=True)
    author = CustomUserNestedSerializer(read_only=True)
    replies = ReplyNestedSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ['url', 'post', 'author', 'comment', 'replies', 'commented_at', 'updated_at']


class CommentReplyListSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserNestedSerializer(read_only=True)
    addsign_detail = ReplyNestedSerializer(read_only=True, source='addsign')
    adds_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reply
        fields = [
            'url', 'author', 'addsign', 'addsign_detail', 'reply', 'adds_count',
            'replied_at', 'updated_at',
        ]
        extra_kwargs = {
            'addsign': {'write_only': True},
        }

    def get_adds_count(self, obj):
        return obj.adds.count()


class ReplyDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserNestedSerializer(read_only=True)
    addsign = ReplyNestedSerializer(read_only=True)
    adds = ReplyNestedSerializer(read_only=True, many=True)

    class Meta:
        model = Reply
        fields = ['url', 'author', 'comment', 'addsign', 'reply', 'adds', 'replied_at', 'updated_at']
        extra_kwargs = {
            'comment': {'read_only': True, }
        }


class ReplyAddsListSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomUserNestedSerializer(read_only=True)
    adds_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'url', 'author', 'reply', 'adds_count', 'replied_at', 'updated_at',
        ]

    def get_adds_count(self, obj):
        return obj.adds.count()

