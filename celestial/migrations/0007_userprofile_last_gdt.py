# Generated by Django 4.1.7 on 2023-03-11 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_userprofile_interacted'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_gdt',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 11, 10, 49, 42, 925490)),
        ),
    ]
