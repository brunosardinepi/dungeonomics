# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_auto_20161108_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]