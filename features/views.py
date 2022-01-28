from features import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class FeatureList(generics.ListAPIView):
    serializer_class = serializers.FeatureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        features = models.Feature.objects.all()
        return sorted(features, key=lambda i: i.vote_count, reverse=True)
