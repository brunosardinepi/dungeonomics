# Generated by Django 2.0.9 on 2018-11-12 20:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('characters', '0025_auto_20181111_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalcharacter',
            name='importers',
            field=models.ManyToManyField(related_name='character_importers', to=settings.AUTH_USER_MODEL),
        ),
    ]
