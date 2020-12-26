# Generated by Django 3.1.1 on 2020-11-12 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_delete_invoice'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communication', '0013_delete_talk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artitcle', models.ManyToManyField(related_name='talks', to='store.Article')),
                ('users', models.ManyToManyField(related_name='talks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MessageText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.IntegerField()),
                ('recipient_id', models.IntegerField()),
                ('content', models.TextField()),
                ('talk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='communication.talk')),
            ],
        ),
    ]
