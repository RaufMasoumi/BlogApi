from rest_framework import serializers


class CustomUserNestedSerializer(serializers.Serializer):
    profile = serializers.HyperlinkedIdentityField(view_name='user-detail')
    username = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass