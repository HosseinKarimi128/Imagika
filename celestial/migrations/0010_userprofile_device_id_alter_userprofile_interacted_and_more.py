# Generated by Django 4.1.7 on 2023-03-11 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_midscorequeue_lowscorequeue_highscorequeue'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='device_id',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='interacted',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='shown_name',
            field=models.CharField(max_length=100),
        ),
    ]
