# Generated by Django 5.0.7 on 2024-10-23 06:26

import django.db.models.deletion
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Builder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('website', models.CharField(blank=True, max_length=300, null=True)),
                ('details', models.TextField(blank=True, max_length=300, null=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('country_lat', models.CharField(blank=True, max_length=200, null=True)),
                ('country_long', models.CharField(blank=True, max_length=200, null=True)),
                ('country_details', tinymce.models.HTMLField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('city_lat', models.CharField(blank=True, max_length=200, null=True)),
                ('city_long', models.CharField(blank=True, max_length=200, null=True)),
                ('city_details', tinymce.models.HTMLField(blank=True, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='vacationprojects.country')),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(max_length=100)),
                ('meta_description', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=500)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('storeys', models.CharField(max_length=200)),
                ('total_units', models.CharField(max_length=200)),
                ('price_starts', models.FloatField(blank=True, null=True)),
                ('price_end', models.FloatField(blank=True, null=True)),
                ('description', tinymce.models.HTMLField()),
                ('project_address', models.CharField(max_length=400)),
                ('postal_code', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=200)),
                ('longitude', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('Upcoming', 'Upcoming'), ('Selling', 'Selling'), ('Planning Phase', 'Planning Phase'), ('Sold out', 'Sold out')], default='Selling', max_length=200)),
                ('project_type', models.CharField(choices=[('Villa', 'Villa'), ('Apartment', 'Apartment'), ('Townhouse', 'Townhouse'), ('Resort', 'Resort'), ('Other', 'Other')], default='Villa', max_length=200)),
                ('street_map', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='project_images/')),
                ('is_featured', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('builder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='vacationprojects.builder')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='vacationprojects.city')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='project_documents/')),
                ('title', models.CharField(max_length=200)),
                ('document_type', models.CharField(blank=True, max_length=100)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='vacationprojects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='project_images/')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vacationprojects.project')),
            ],
        ),
    ]