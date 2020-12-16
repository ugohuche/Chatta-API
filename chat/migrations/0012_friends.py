# Generated by Django 3.1 on 2020-10-31 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_delete_friendedcontacts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='chat.contact')),
                ('friends', models.ManyToManyField(blank=True, to='chat.Contact')),
            ],
        ),
    ]