# Generated by Django 3.1.6 on 2021-02-19 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='profilename',
            new_name='username',
        ),
    ]
