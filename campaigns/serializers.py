from campaigns import models
from rest_framework import serializers


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Campaign
        fields = ['id', 'content', 'title', 'created_at']
