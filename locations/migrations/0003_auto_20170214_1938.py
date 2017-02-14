# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-14 19:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0002_auto_20170214_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='World',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RenameField(
            model_name='location',
            old_name='parent',
            new_name='parent_location',
        ),
        migrations.AddField(
            model_name='location',
            name='world',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='locations.World'),
            preserve_default=False,
        ),
    ]
