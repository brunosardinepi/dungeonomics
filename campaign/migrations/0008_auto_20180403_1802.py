# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-03 18:02
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0007_auto_20180403_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='public_url',
            field=models.CharField(default=uuid.uuid4, max_length=255, unique=True),
        ),
    ]