# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-04 20:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='description',
            new_name='content',
        ),
    ]