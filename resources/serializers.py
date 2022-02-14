from resources import models
from rest_framework import serializers


class ResourceSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = models.Resource
        fields = ['id', 'user', 'name', 'link']

    def get_link(self, obj):
        print(f"obj = {obj}")
        print(f"obj.get_absolute_url() = {obj.get_absolute_url()}")
        return obj.get_absolute_url()
