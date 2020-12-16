# Generated by Django 3.1 on 2020-10-31 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_auto_20201031_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='chatType',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='city',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='contact',
            name='fullname',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_type',
            field=models.CharField(default='text', max_length=20),
        ),
    ]
