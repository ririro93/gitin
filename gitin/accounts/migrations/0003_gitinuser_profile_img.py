# Generated by Django 3.1.6 on 2021-02-17 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210217_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitinuser',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile_img/'),
        ),
    ]
