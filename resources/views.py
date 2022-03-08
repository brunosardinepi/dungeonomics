from resources import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


def assign_resource_to_group(resource, group_name):
    """
    Create the resource group if it doesn't exist, then
    assign the resource to it.
    """

    # Check if the resource group exists and create it if needed.
    try:
        group = models.ResourceGroup.objects.get(user=resource.user, name=group_name)
    except models.ResourceGroup.DoesNotExist:
        group = models.ResourceGroup.objects.create(user=resource.user, name=group_name)

    # Assign the resource to the group.
    group.resources.add(resource)

class ResourceAttributesList(generics.ListAPIView):
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
        print("self.request", self.request)
        print("self.request.data", self.request.data)
        if "parent" in self.request.data and self.request.data['parent'] != "":
            parent = models.Resource.objects.get(pk=self.request.data['parent'])
        else:
            parent = None

        resource = serializer.save(
            user=self.request.user,
            parent=parent,
        )

        if "tags" in self.request.data:
            print(self.request.data['tags'])
            print(f"resource = {resource}")
            tags = self.request.data['tags'].split(",")
            print(f"tags = {tags}")
            tags = [i.strip() for i in tags]
            print(f"tags = {tags}")
            for tag in tags:
                assign_resource_to_group(resource, tag)

class ResourceDelete(generics.DestroyAPIView):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

class ResourceDetail(generics.RetrieveAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user)

class ResourceGroupList(generics.ListAPIView):
    serializer_class = serializers.ResourceGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.ResourceGroup.objects.filter(user=self.request.user)

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

    def perform_update(self, serializer):
        print("self.request", self.request)
        print("self.request.data", self.request.data)
        if "parent" in self.request.data and self.request.data['parent'] != "":
            parent = models.Resource.objects.get(pk=self.request.data['parent'])
        else:
            parent = None

        resource = serializer.save(
            user=self.request.user,
            parent=parent,
        )

        if "tags" in self.request.data:
            print(self.request.data['tags'])
            print(f"resource = {resource}")
            tags = self.request.data['tags'].split(",")
            print(f"tags = {tags}")
            tags = [i.strip() for i in tags]
            print(f"tags = {tags}")
            for tag in tags:
                assign_resource_to_group(resource, tag)
