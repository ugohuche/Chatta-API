# Generated by Django 3.1 on 2020-11-04 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_chat_admins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='admins',
            field=models.ManyToManyField(related_name='chatAdmins', to='chat.Contact'),
        ),
    ]
