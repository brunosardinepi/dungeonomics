# Generated by Django 3.2.6 on 2021-08-17 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0024_auto_20210810_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='name',
        ),
    ]
