from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from dungeonomics.config import settings as secrets


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    item_type = models.CharField(verbose_name= _('Type'), max_length=255, default='', blank=True)
    rarity = models.CharField(max_length=255, default='', blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items:item_detail', kwargs={
            'item_pk': self.pk
            })

    @property
    def mention(self):
        return f"[{self.__str__()}]({secrets['site']}{self.get_absolute_url()})"
