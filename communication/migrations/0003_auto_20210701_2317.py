# Generated by Django 3.1.1 on 2021-07-01 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0002_auto_20210701_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='article',
        ),
        migrations.RemoveField(
            model_name='notifmessage',
            name='article',
        ),
    ]
