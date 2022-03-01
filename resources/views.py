from resources import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ResourceChildrenList(generics.ListAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(
            user=self.request.user,
            parent__pk=self.kwargs['pk'],
        )

class ResourceCreate(generics.CreateAPIView):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if "parent" in self.request.data:
            parent = models.Resource.objects.get(pk=self.request.data['parent'])
        else:
            parent = None

        serializer.save(
            user=self.request.user,
            parent=parent,
        )

class ResourceDelete(generics.DestroyAPIView):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

class ResourceDetail(generics.RetrieveAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user)

class ResourceList(generics.ListAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(
            user=self.request.user,
            parent__isnull=True,
        )

class ResourceUpdate(generics.UpdateAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user)

