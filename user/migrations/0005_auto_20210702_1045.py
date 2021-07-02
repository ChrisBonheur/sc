# Generated by Django 3.1.1 on 2021-07-02 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210702_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='airtel_money',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profil',
            name='contact_airtel',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profil',
            name='contact_mtn',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profil',
            name='gender',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.gender'),
        ),
        migrations.AlterField(
            model_name='profil',
            name='mtn_money',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profil',
            name='whatsap_number',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]