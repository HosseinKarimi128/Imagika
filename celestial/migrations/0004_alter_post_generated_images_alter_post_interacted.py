# Generated by Django 4.1.7 on 2023-04-09 10:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celestial', '0003_topic_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='generated_images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='post',
            name='interacted',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None),
        ),
    ]
