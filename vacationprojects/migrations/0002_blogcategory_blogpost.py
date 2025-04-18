# Generated by Django 5.0.7 on 2024-10-23 08:50

import django.db.models.deletion
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacationprojects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Blog Categories',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('meta_title', models.CharField(max_length=100)),
                ('meta_description', models.CharField(max_length=200)),
                ('thumbnail', models.ImageField(upload_to='blog_thumbnails/')),
                ('content', tinymce.models.HTMLField()),
                ('excerpt', models.TextField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(related_name='posts', to='vacationprojects.blogcategory')),
                ('cities', models.ManyToManyField(blank=True, help_text='Cities related to this blog post', related_name='blog_posts', to='vacationprojects.city')),
                ('countries', models.ManyToManyField(blank=True, help_text='Countries related to this blog post', related_name='blog_posts', to='vacationprojects.country')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
