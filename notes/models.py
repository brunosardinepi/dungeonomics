from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

from campaign.models import Campaign


class Note(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    content = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'notes:note_detail',
            kwargs={'note_pk': self.pk},
        )
