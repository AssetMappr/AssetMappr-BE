"""Serializer for user"""
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:  # pylint: disable=too-few-public-methods
        """User meta"""
        model = Users
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create user"""
        password = validated_data.pop('password')
        user = Users.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        """Representation for token"""
        refresh = RefreshToken.for_user(instance)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        representation = super().to_representation(instance)
        representation['tokens'] = tokens
        return representation
