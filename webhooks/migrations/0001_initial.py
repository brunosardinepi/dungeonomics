# Generated by Django 2.0.10 on 2019-01-24 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=1024)),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webhooks.Webhook')),
            ],
        ),
    ]
