from django.db import models
import json

class Developer(models.Model):
    name = models.CharField(max_length=300)
    website = models.CharField(max_length=300, null=True, blank=True)
    details = models.TextField(max_length=300, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class PreConstruction(models.Model):

    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Selling", "Selling"),
        ("Planning Phase", "Planning Phase"),
        ("Sold out", "Sold out")
    ]
    PROJECT_CHOICES = [
        ("Condo", "Condo"),
        ("Townhome", "Townhome"),
        ("Semi-Detached", "Semi-Detached"),
        ("Detached", "Detached"),
        ("NaN", "NaN"),
    ]
     
    meta_title = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=200)
    project_name = models.CharField(max_length=500)
    slug = models.CharField(max_length=200, null=True, blank=True)
    storeys = models.CharField(max_length=200)
    total_units = models.CharField(max_length=200)
    price_starts = models.FloatField(null=True, blank=True)
    price_end = models.FloatField(null=True, blank=True)
    description = models.TextField()
    project_address = models.CharField(max_length=400)
    postal_code = models.CharField(max_length=200)  
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    occupancy = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="Selling")
    project_type = models.CharField(max_length=200, choices=PROJECT_CHOICES, default="Condo")
    street_map = models.TextField()
    developer= models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='preconstructions')
    city = models.ForeignKey("City", on_delete=models.CASCADE, related_name='preconstructions')
    image= models.ImageField(upload_to='preconstruction_images/', blank=True, null=True, default='')
    
    def __str__(self):
        return self.project_name
    
class City(models.Model):

    name = models.CharField(max_length=200)
    city_lat = models.CharField(max_length=200, null=True, blank=True)
    city_long = models.CharField(max_length=200, null=True, blank=True)
    city_details = models.TextField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name
    


class PreConstructionImage(models.Model):
    preconstruction = models.ForeignKey(PreConstruction, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(null=True, blank=True, upload_to='preconstruction_images/', default="")