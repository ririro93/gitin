# Generated by Django 3.1.6 on 2021-02-20 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitAPI', '0004_auto_20210220_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='githubrepo',
            name='html_url',
        ),
    ]
