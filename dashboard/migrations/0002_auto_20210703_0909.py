# Generated by Django 3.1.1 on 2021-07-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='airtel_account_number',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='mtn_account_number',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
