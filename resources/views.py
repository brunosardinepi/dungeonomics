from resources import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ResourceDetail(generics.RetrieveAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user)

class ResourceList(generics.ListAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user)
