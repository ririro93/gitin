# Generated by Django 3.1.6 on 2021-02-18 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitAPI', '0008_auto_20210218_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repocomment',
            name='content',
            field=models.CharField(max_length=400),
        ),
    ]
