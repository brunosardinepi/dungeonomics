from collections import OrderedDict

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Feature(models.Model):
    description = models.TextField()
    new = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    def votes(self):
        return Vote.objects.filter(feature=self).count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    feature = models.ForeignKey('votes.Feature', on_delete=models.CASCADE)