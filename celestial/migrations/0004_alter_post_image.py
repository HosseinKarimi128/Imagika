# Generated by Django 4.1.7 on 2023-03-19 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celestial', '0003_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
