# Generated by Django 3.1.6 on 2021-02-21 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitAPI', '0008_repocommit_committed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='repocommit',
            name='message',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
    ]
