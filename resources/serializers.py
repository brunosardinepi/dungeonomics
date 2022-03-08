from resources import models
from rest_framework import serializers


class ResourceSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
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
            'groups',
        ]

    def get_groups(self, obj):
#        return list(obj.resourcegroup_set.all().values())
        group_names = list(
            obj.resourcegroup_set.all().values_list('name', flat=True).order_by('name')
        )
        return ", ".join(group_names)

    def get_link(self, obj):
        return obj.get_absolute_url()

class ResourceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResourceGroup
        fields = [
            'id',
            'name',
            'resources',
        ]
