# Generated by Django 3.1.1 on 2021-05-19 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_auto_20210519_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_share', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Partage sur réseaux sociaux',
            },
        ),
        migrations.CreateModel(
            name='SocialApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Applications sociales de partage',
            },
        ),
        migrations.RemoveField(
            model_name='favourite',
            name='article',
        ),
        migrations.RemoveField(
            model_name='favourite',
            name='date_add',
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='favourite',
            name='articles',
            field=models.ManyToManyField(related_name='favourites', to='store.Article'),
        ),
        migrations.AlterField(
            model_name='favourite',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.AddField(
            model_name='share',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.article'),
        ),
        migrations.AddField(
            model_name='share',
            name='social_app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.socialapp'),
        ),
    ]
