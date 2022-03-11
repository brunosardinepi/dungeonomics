from resources import models
from rest_framework import serializers


class ResourceSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = models.Resource
        fields = [
            'id',
            'name',
            'content',
            'created_at',
            'parent',
            'groups',
        ]

    def get_groups(self, obj):
        group_names = list(
            obj.resourcegroup_set.all().values_list('name', flat=True).order_by('name')
        )
        return ", ".join(group_names)

class ResourceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResourceGroup
        fields = [
            'id',
            'name',
            'resources',
        ]
