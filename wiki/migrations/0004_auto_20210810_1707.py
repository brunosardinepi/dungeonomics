# Generated by Django 3.2.6 on 2021-08-10 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0003_auto_20181031_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]