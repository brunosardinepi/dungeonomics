from campaigns import models
from rest_framework import serializers


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Campaign
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = '__all__'
