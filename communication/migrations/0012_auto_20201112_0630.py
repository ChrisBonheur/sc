# Generated by Django 3.1.1 on 2020-11-12 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0011_talk_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='message',
            name='talk',
        ),
    ]
