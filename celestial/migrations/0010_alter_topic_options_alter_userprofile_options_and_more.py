# Generated by Django 4.1.7 on 2023-04-15 11:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celestial', '0009_remove_post_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['-starts_on', 'title'], 'verbose_name': 'topic', 'verbose_name_plural': 'topics'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['shown_name'], 'verbose_name': 'UserProfile', 'verbose_name_plural': 'UserProfiles'},
        ),
        migrations.AlterField(
            model_name='post',
            name='generated_images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), editable=False, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='post',
            name='uploaded_image',
            field=models.UUIDField(default=None, null=True),
        ),
    ]
