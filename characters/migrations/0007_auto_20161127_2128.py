# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0006_auto_20161121_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monster',
            name='actions',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='monster',
            name='traits',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='npc',
            name='actions',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='npc',
            name='traits',
            field=models.TextField(default=''),
        ),
    ]
