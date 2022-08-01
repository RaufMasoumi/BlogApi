from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', )

