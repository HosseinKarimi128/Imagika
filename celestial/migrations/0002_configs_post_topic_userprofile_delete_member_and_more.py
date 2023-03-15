# Generated by Django 4.1.7 on 2023-03-09 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='configs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=250)),
                ('prompt', models.TextField(default='Create a post.')),
                ('n_prompt', models.TextField(blank=True, null=True)),
                ('uploaded_image', models.UUIDField(default=None, editable=False, null=True)),
                ('generated_image', models.UUIDField(default=None, editable=False, null=True)),
                ('draft', models.BooleanField(default=True)),
                ('publish', models.DateField(null=True)),
                ('dislike_count', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-publish', 'prompt'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('strts_on', models.DateTimeField(blank=True, null=True)),
                ('finished_on', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shown_name', models.CharField(max_length=500)),
                ('intracted', models.CharField(max_length=500, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='celestial.topic'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
