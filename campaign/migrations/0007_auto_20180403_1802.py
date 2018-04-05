# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-03 18:02
from __future__ import unicode_literals

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    Campaign = apps.get_model('campaign', 'Campaign')
    for row in Campaign.objects.all():
        row.public_url = uuid.uuid4()
        row.save(update_fields=['public_url'])

class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0006_campaign_public_url'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
