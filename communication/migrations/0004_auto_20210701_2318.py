# Generated by Django 3.1.1 on 2021-07-01 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0003_auto_20210701_2317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talk',
            old_name='date_create',
            new_name='date_last_message_added',
        ),
    ]