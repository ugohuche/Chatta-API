# Generated by Django 3.1 on 2020-10-31 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_auto_20201031_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='slug',
            field=models.SlugField(default='ugoh'),
        ),
    ]
