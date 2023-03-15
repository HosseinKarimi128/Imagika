# Generated by Django 4.1.7 on 2023-03-11 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_userprofile_last_gdt'),
    ]

    operations = [
        migrations.CreateModel(
            name='MidScoreQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LowScoreQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HighScoreQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
