from resources import models
from rest_framework import serializers


class ResourceSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = models.Resource
        fields = [
            'id',
            'name',
            'link',
            'content',
            'created_at',
            'parent',
        ]

    def get_link(self, obj):
        return obj.get_absolute_url()
