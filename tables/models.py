from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.urls import reverse
from django.db import models

from dungeonomics import config


class Table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tables:table_detail', kwargs={'table_pk': self.pk})

    def get_full_url(self):
        protocol = config.settings['protocol']
        domain = Site.objects.get_current().domain
        path = reverse('tables:table_detail', kwargs={'table_pk': self.pk})
        return "{}://{}{}".format(protocol, domain, path)

    def options(self):
        return self.tableoption_set.all().order_by('pk')


class TableOption(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, default='')

    def __str__(self):
        return "{}: {}".format(self.table, self.content[:10])
