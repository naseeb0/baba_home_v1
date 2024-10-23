from django.db import models
from django.conf import settings
from django.utils.text import slugify
from tinymce.models import HTMLField

class Builder(models.Model):
    name = models.CharField(max_length=300)
    website = models.CharField(max_length=300, null=True, blank=True)
    details = models.TextField(max_length=300, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Country(models.Model):
    name = models.CharField(max_length=200)
    country_lat = models.CharField(max_length=200, null=True, blank=True)
    country_long = models.CharField(max_length=200, null=True, blank=True)
    country_details = HTMLField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=200)
    city_lat = models.CharField(max_length=200, null=True, blank=True)
    city_long = models.CharField(max_length=200, null=True, blank=True)
    city_details = HTMLField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}, {self.country.name}"
    
    class Meta:
        verbose_name_plural = "Cities"

class Project(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Selling", "Selling"),
        ("Planning Phase", "Planning Phase"),
        ("Sold out", "Sold out")
    ]
    PROJECT_CHOICES = [
        ("Villa", "Villa"),
        ("Apartment", "Apartment"),
        ("Townhouse", "Townhouse"),
        ("Resort", "Resort"),
        ("Other", "Other"),
    ]
     
    meta_title = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=200)
    project_name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    storeys = models.CharField(max_length=200)
    total_units = models.CharField(max_length=200)
    price_starts = models.FloatField(null=True, blank=True)
    price_end = models.FloatField(null=True, blank=True)
    description = HTMLField()
    project_address = models.CharField(max_length=400)
    postal_code = models.CharField(max_length=200)  
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="Selling")
    project_type = models.CharField(max_length=200, choices=PROJECT_CHOICES, default="Villa")
    street_map = models.TextField()
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE, related_name='projects')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='projects')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='projects', null=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.project_name)
            counter = 1
            self.slug = base_slug
            while Project.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='project_images/')
    title = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for {self.project.project_name}"

class ProjectDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to='project_documents/')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=100, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.project.project_name}"