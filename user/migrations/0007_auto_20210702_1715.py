# Generated by Django 3.1.1 on 2021-07-02 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210702_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='contact_mtn',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
