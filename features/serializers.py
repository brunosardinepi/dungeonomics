from features import models
from rest_framework import serializers


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feature
#        fields = '__all__'
        fields = ('id', 'description', 'new', 'vote_count')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = '__all__'
