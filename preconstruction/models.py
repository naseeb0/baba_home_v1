from django.db import models
import json
from django.conf import settings
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class Developer(models.Model):
    name = models.CharField(max_length=300)
    website = models.CharField(max_length=300, null=True, blank=True)
    details = models.TextField(max_length=300, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    sales_office_address = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sales_person_name = models.CharField(max_length=300, null=True, blank=True)
    sales_person_contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class PreConstruction(models.Model):

    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Selling", "Selling"),
        ("Planning Phase", "Planning Phase"),
        ("Sold out", "Sold out"),
        ("Move-in ready", "Move-in ready"),
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
    description = HTMLField()
    deposit_structure = HTMLField(null=True, blank=True)
    incentives = HTMLField(null=True, blank=True)
    project_completion = models.CharField(max_length=200, null=True, blank=True)
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
    created = models.DateTimeField(auto_now_add=True)
    image= models.ImageField(upload_to='preconstruction_images/', blank=True, null=True, default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='preconstructions',null=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    floorplan = models.ImageField(upload_to='floorplans/', blank=True, null=True, default='')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_name)
            # Handle duplicate slugs
            original_slug = self.slug
            counter = 1
            while PreConstruction.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_floor_plans(self):
        """Get all floor plans for this project"""
        return self.floor_plan_images.all()
    
    def get_floor_plans_by_category(self, category):
        """Get floor plans for a specific category"""
        return self.floor_plan_images.filter(category=category)
    
    def get_floor_plan_categories(self):
        """Get list of categories that have floor plans"""
        return self.floor_plan_images.values_list('category', flat=True).distinct()
    
    def add_floor_plan(self, image, category, name=None, square_footage=None):
        """Helper method to add a new floor plan"""
        return self.floor_plan_images.create(
            image=image,
            category=category,
            name=name or f"{self.project_name} - {category}",
            square_footage=square_footage
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_name)
            original_slug = self.slug
            counter = 1
            while PreConstruction.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_name
    
class FloorPlan(models.Model):
    CATEGORY_CHOICES = [
        ("1BED", "1 Bedroom"),
        ("2BED", "2 Bedroom"),
        ("3BED", "3 Bedroom"),
        ("4BED", "4 Bedroom"),
        ("OTHER", "Other")
    ]
    
    preconstruction = models.ForeignKey(
        PreConstruction, 
        on_delete=models.CASCADE,
        related_name='floor_plan_images'  
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES
    )
    image = models.ImageField(
        upload_to='floorplans/',
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100)
    square_footage = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        if self.image:
            return f"{settings.MEDIA_URL}{self.image}"
        return None

    class Meta:
        ordering = ['category', 'created']

    def __str__(self):
        return f"{self.preconstruction.project_name} - {self.get_category_display()} - {self.name}"

class FloorPlanDocs(models.Model):
    preconstruction = models.ForeignKey(PreConstruction, on_delete=models.CASCADE, related_name='floorplan_docs')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to='floorplan_docs/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'svg', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Floor Plan Document"
        verbose_name_plural = "Floor Plan Documents"

    def __str__(self):
        return f"{self.title} - {self.preconstruction.project_name}"

class Feature(models.Model):
    preconstruction = models.ForeignKey(PreConstruction, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to='features/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'svg', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.preconstruction.project_name}"

class SampleAPS(models.Model):
    preconstruction = models.ForeignKey(PreConstruction, on_delete=models.CASCADE, related_name='sample_aps')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to='sample_aps/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'svg', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sample APS"
        verbose_name_plural = "Sample APS"

    def __str__(self):
        return f"{self.title} - {self.preconstruction.project_name}"

class Siteplan(models.Model):
    preconstruction = models.ForeignKey(PreConstruction, on_delete=models.CASCADE, related_name='siteplans')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to='siteplans/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png', 'svg', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.preconstruction.project_name}"

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


class PreConstructionFloorPlans(models.Model):
    preconstruction = models.ForeignKey(PreConstruction, on_delete=models.CASCADE, related_name="floorplans")
    floorplan = models.ImageField(null=True, blank=True, upload_to='floorplans/', default="")

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)
    thumbnail = models.ImageField(upload_to='blog_thumbnails/', blank=True, null=True)

    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id or self._state.adding:
            base_slug = slugify(self.title)
            counter = 1
            self.slug = base_slug
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
                
        if not self.meta_title:
            self.meta_title = self.title[:100]
            
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
