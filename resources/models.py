from django.contrib.auth.models import User
from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('resources:resource_detail', kwargs={'pk': self.pk})
