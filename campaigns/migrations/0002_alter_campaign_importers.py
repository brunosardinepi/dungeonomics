# Generated by Django 3.2.11 on 2022-01-28 21:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='importers',
            field=models.ManyToManyField(blank=True, related_name='importers', to=settings.AUTH_USER_MODEL),
        ),
    ]
