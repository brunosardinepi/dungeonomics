from features import models
from rest_framework import serializers


class FeatureSerializer(serializers.ModelSerializer):
    has_user_vote = serializers.SerializerMethodField()

    class Meta:
        model = models.Feature
        fields = ('id', 'description', 'new', 'vote_count', 'has_user_vote')

    def get_has_user_vote(self, obj):
        if self.context.get('request') and self.context['request'].user:
            return obj.has_user_vote(self.context['request'].user)
        return

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = '__all__'
