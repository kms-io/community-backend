from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser
from .managers import CustomUserManager


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'user_name', 'password', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            user_name=validated_data['user_name'],
            password=validated_data['password']
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self, user):
        CustomUserManager().set_password(
            user=user,
            old_password=self.validated_data['old_password'],
            new_password=self.validated_data['new_password']
        )
        return user
