# Generated by Django 3.1 on 2020-10-17 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20201017_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendedcontacts',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='chat.contact'),
        ),
    ]