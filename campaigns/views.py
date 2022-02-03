from campaigns import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class CampaignDetail(generics.RetrieveAPIView):
    queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated]

class CampaignList(generics.ListAPIView):
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Campaign.objects.filter(user=self.request.user)

class ChapterList(generics.ListAPIView):
    serializer_class = serializers.ChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        campaign = models.Campaign.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        return campaign.chapter_set.all()
