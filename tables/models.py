from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tables:table_detail',
            kwargs={'table_pk': self.pk}
        )


class TableOption(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    option = models.CharField(max_length=255, default='')

    def __str__(self):
        return "{}: {}".format(table, option[:10])