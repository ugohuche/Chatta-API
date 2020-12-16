# Generated by Django 3.1 on 2020-11-03 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_auto_20201031_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='is_recieved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='is_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chat',
            name='chatName',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='chat',
            name='chatType',
            field=models.CharField(choices=[('DM', 'Direct Message'), ('GC', 'Group Chat')], default='GC', max_length=3),
        ),
    ]