# Generated by Django 3.1.1 on 2021-05-08 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('recipient_id', models.IntegerField(verbose_name='Recevreur')),
                ('type_msg', models.CharField(choices=[('message', 'Message')], default='notif', max_length=100)),
                ('date_send', models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoie")),
                ('readed', models.BooleanField(default=False)),
                ('link', models.CharField(max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Message',
                'ordering': ('-date_send',),
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1_id', models.IntegerField()),
                ('user2_id', models.IntegerField()),
                ('last_message_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Conversation',
                'ordering': ('-last_message_date',),
            },
        ),
        migrations.CreateModel(
            name='MessageText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.IntegerField()),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('seen', models.BooleanField(default=False)),
                ('alert_play', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('talk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='communication.talk')),
            ],
            options={
                'verbose_name': 'Message texte',
                'ordering': ('date',),
            },
        ),
    ]
