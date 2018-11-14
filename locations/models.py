import os
import random
import string

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from dungeonomics import config


def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "media/user/images/%s.%s" % (create_random_string(), ext)
    return filename

class LocationTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=upload_to,
        max_length=255,
        blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class World(LocationTemplate):
    class Meta:
        ordering = ['name',]

    def get_absolute_url(self):
        return reverse('locations:location_detail', kwargs={'world_pk': self.pk})

    def get_full_url(self):
        protocol = config.settings['protocol']
        domain = Site.objects.get_current().domain
        path = reverse('locations:location_detail', kwargs={'world_pk': self.pk})
        return "{}://{}{}".format(protocol, domain, path)


class Location(LocationTemplate):
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    parent_location = models.ForeignKey("self",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['name',]

    def get_absolute_url(self):
        return reverse('locations:location_detail', kwargs={'location_pk': self.pk})

    def get_full_url(self):
        protocol = config.settings['protocol']
        domain = Site.objects.get_current().domain
        path = reverse('locations:location_detail', kwargs={'location_pk': self.pk})
        return "{}://{}{}".format(protocol, domain, path)

@receiver(pre_save, sender=World)
def delete_old_world_image(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = World.objects.get(pk=instance.pk).image
    except World.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if old_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

@receiver(pre_save, sender=Location)
def delete_old_location_image(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Location.objects.get(pk=instance.pk).image
    except Location.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if old_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

@receiver(post_delete, sender=World)
def auto_delete_world_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_delete, sender=Location)
def auto_delete_location_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
