# Generated by Django 3.1.6 on 2021-02-20 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitAPI', '0003_repocontentfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repocontentfile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='repocontentfile',
            name='sha',
        ),
        migrations.RemoveField(
            model_name='repocontentfile',
            name='size',
        ),
    ]