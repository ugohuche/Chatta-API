# Generated by Django 3.1 on 2020-10-31 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contactFriends', to='chat.contact'),
        ),
    ]
