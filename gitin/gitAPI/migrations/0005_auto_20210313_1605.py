# Generated by Django 3.1.6 on 2021-03-13 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitAPI', '0004_githubrepo_refreshed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepo',
            name='refreshed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
