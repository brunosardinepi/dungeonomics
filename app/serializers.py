from app import models
from django.contrib.auth.models import User
from rest_framework import serializers


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PasswordReset
        fields = [
            'uuid',
            'created_at',
            'is_completed',
            'email',
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
