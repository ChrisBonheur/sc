# Generated by Django 3.1.1 on 2021-07-26 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20210703_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='airtel_account_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='mtn_account_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
