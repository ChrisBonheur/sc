# Generated by Django 3.1.1 on 2021-07-02 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0006_auto_20210702_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifmessage',
            name='link',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
