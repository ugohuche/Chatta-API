# Generated by Django 3.1 on 2020-11-12 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0020_auto_20201104_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, help_text="It's always nice to add a friendly message", max_length=300, verbose_name='Optional message')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_sent', to='chat.contact')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_recieved', to='chat.contact', verbose_name='User to invite')),
            ],
        ),
    ]