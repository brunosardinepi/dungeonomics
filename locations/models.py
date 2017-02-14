from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('locations:location_detail', kwargs={
            'location_pk': self.pk
            })

