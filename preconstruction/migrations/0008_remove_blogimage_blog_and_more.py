# Generated by Django 5.0.7 on 2024-10-23 04:58

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0007_blogpost_views_count_alter_blogpost_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogimage',
            name='blog',
        ),
        migrations.RemoveIndex(
            model_name='blogpost',
            name='preconstruc_created_19b30d_idx',
        ),
        migrations.RemoveIndex(
            model_name='blogpost',
            name='preconstruc_slug_11de45_idx',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='featured_image',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
        migrations.DeleteModel(
            name='BlogImage',
        ),
    ]
