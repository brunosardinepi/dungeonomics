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
        if self.kwargs['pk'] == 1:
            resources = models.Resource.objects.filter(
                user__username="example",
                parent__pk=self.kwargs['pk'],
            )
        else:
            resources = models.Resource.objects.filter(
                user=self.request.user,
                parent__pk=self.kwargs['pk'],
            )
        return resources

class ResourceCreate(generics.CreateAPIView):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if "parent" in self.request.data and self.request.data['parent'] != "":
            try:
                parent = models.Resource.objects.get(
                    user=self.request.user,
                    pk=self.request.data['parent'],
                )
            except models.Resource.DoesNotExist:
                return
        else:
            parent = None

        resource = serializer.save(
            user=self.request.user,
            parent=parent,
        )

        if "tags" in self.request.data:
            tags = self.request.data['tags'].split(",")
            tags = [i.strip() for i in tags]
            for tag in tags:
                assign_resource_to_group(resource, tag)

class ResourceDelete(generics.DestroyAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        # If this was the last resource in a resource group,
        # delete the resource group.
        for group in instance.resourcegroup_set.all():
            if not group.resources.all().exclude(pk=instance.pk):
                group.delete()
        super().perform_destroy(instance)

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
        resources = models.Resource.objects.filter(
            user=self.request.user,
            parent__isnull=True,
        )
        if not resources:
            resources = models.Resource.objects.filter(
                user__username="example",
                parent__isnull=True,
            )
        return resources

class ResourceUpdate(generics.UpdateAPIView):
    serializer_class = serializers.ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if "parent" in self.request.data and self.request.data['parent'] != "":
            try:
                parent = models.Resource.objects.get(
                    user=self.request.user,
                    pk=self.request.data['parent'],
                )
            except models.Resource.DoesNotExist:
                return
        else:
            parent = None

        resource = serializer.save(
            user=self.request.user,
            parent=parent,
        )

        if "tags" in self.request.data:
            tags = self.request.data['tags'].split(",")
            tags = [i.strip() for i in tags]
            for tag in tags:
                assign_resource_to_group(resource, tag)
