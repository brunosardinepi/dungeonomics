from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Webhook(models.Model):
    provider = models.CharField(max_length=100)

    def __str__(self):
        return "{}:{}".format(self.provider, self.pk)

    def get_absolute_url(self):
        return reverse('webhooks:webhook_detail', kwargs={'pk': self.pk})

class WebhookAttribute(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=1024)
