# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-02 20:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tableoption',
            old_name='option',
            new_name='description',
        ),
    ]
