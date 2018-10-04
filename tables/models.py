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

    def options(self):
        return self.tableoption_set.all().order_by('pk')


class TableOption(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return "{}: {}".format(self.table, self.description[:10])