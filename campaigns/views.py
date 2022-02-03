from campaigns import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class CampaignCreate(generics.CreateAPIView):
    queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CampaignDelete(generics.DestroyAPIView):
    queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated]

class CampaignDetail(generics.RetrieveAPIView):
    queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated]

class CampaignList(generics.ListAPIView):
    serializer_class = serializers.CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Campaign.objects.filter(user=self.request.user)
