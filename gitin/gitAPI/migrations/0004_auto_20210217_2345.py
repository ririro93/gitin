# Generated by Django 3.1.6 on 2021-02-17 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gitAPI', '0003_auto_20210217_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitinUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='githubuser',
            name='gitinuser',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gitAPI.gitinuser'),
        ),
    ]
