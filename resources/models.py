from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('resources:resource_detail', kwargs={'pk': self.pk})
