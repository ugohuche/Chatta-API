# Generated by Django 3.1 on 2020-10-29 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20201018_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='fullname',
            field=models.TextField(blank=True),
        ),
    ]
