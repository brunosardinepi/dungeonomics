from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class LocationTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class World(LocationTemplate):
    content = models.TextField(blank=True)

    class Meta:
        ordering = ['name',]

    def get_absolute_url(self):
        return reverse('locations:location_detail', kwargs={
            'world_pk': self.pk
            })


class Location(LocationTemplate):
    content = models.TextField(blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name',]

    def get_absolute_url(self):
        return reverse('locations:location_detail', kwargs={
            'world_pk': self.world_id,
            'location_pk': self.pk
            })