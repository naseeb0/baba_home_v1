# Generated by Django 5.0.7 on 2024-12-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0015_preconstruction_incentives'),
    ]

    operations = [
        migrations.AddField(
            model_name='floorplan',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
