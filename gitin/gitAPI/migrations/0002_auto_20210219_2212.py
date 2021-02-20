# Generated by Django 3.1.6 on 2021-02-19 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gitAPI', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='repocomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='repocomment',
            name='repo_connected',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='gitAPI.githubrepo'),
        ),
        migrations.AddField(
            model_name='githubuser',
            name='gitinuser',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='githubrepo',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gitAPI.githubuser'),
        ),
    ]