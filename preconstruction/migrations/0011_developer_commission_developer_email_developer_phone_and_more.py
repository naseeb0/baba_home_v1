# Generated by Django 5.0.7 on 2024-11-30 13:32

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0010_floorplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='commission',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='developer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='developer',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='developer',
            name='sales_office_address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='developer',
            name='sales_person_contact',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='developer',
            name='sales_person_name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='preconstruction',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
