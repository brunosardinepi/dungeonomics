# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 04:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_auto_20161107_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='armor_class',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='monster',
            name='hit_points',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='monster',
            name='saving_throws',
            field=models.CharField(default='adsfasdfasdfasdf', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monster',
            name='skills',
            field=models.CharField(default='asdfasdfasdfasdf', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monster',
            name='speed',
            field=models.CharField(default='asdfasdfasdf', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='npc',
            name='armor_class',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='npc',
            name='hit_points',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='npc',
            name='saving_throws',
            field=models.CharField(default='asdfasdf', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='npc',
            name='skills',
            field=models.CharField(default='asdf', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='npc',
            name='speed',
            field=models.CharField(default='asdf', max_length=255),
            preserve_default=False,
        ),
    ]
