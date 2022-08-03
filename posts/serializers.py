from rest_framework.serializers import ModelSerializer
from .models import Tag, Post, Comment, Reply


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', )


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'description', 'tags', 'created_at', 'updated_at', 'status')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'post', 'comment', 'commented_at', 'updated_at')


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = ('author', 'comment', 'addsign', 'reply', 'replied_at', 'updated_at')

