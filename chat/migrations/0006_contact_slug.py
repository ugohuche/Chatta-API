# Generated by Django 3.1 on 2020-10-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20201017_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='slug',
            field=models.SlugField(default='ugoh'),
        ),
    ]
