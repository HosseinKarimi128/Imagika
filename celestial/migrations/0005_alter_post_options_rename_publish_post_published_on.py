# Generated by Django 4.1.7 on 2023-03-20 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celestial', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-published_on', 'prompt'], 'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='publish',
            new_name='published_on',
        ),
    ]