# Generated by Django 3.1.6 on 2021-02-25 00:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gitAPI', '0013_auto_20210223_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubuser',
            name='last_repos_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]