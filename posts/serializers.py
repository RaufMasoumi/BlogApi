from rest_framework.serializers import ModelSerializer
from .models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'description', 'created_at', 'updated_at', 'status')


