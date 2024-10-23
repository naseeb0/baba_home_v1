from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Builder, Country, City, Project,
    ProjectImage, ProjectDocument
)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'title', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 1
    fields = ['title', 'file', 'document_type', 'upload_date']
    readonly_fields = ['upload_date']

class CityInline(admin.TabularInline):
    model = City
    extra = 1
    fields = ['name', 'city_lat', 'city_long']

@admin.register(Builder)
class BuilderAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'slug']
    search_fields = ['name', 'website']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_lat', 'country_long', 'city_count']
    search_fields = ['name']
    inlines = [CityInline]
    
    def city_count(self, obj):
        return obj.cities.count()
    city_count.short_description = 'Number of Cities'

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city_lat', 'city_long']
    list_filter = ['country']
    search_fields = ['name', 'country__name']
    autocomplete_fields = ['country']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_name', 'builder', 'city', 'status',
        'price_range', 'is_featured', 'is_verified'
    ]
    list_filter = [
        'status', 'project_type', 'is_featured',
        'is_verified', 'created', 'city__country'
    ]
    search_fields = [
        'project_name', 'builder__name',
        'city__name', 'project_address'
    ]
    prepopulated_fields = {'slug': ('project_name',)}
    autocomplete_fields = ['builder', 'city']
    readonly_fields = ['created', 'updated']
    inlines = [ProjectImageInline, ProjectDocumentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'project_name', 'slug', 'builder', 'description',
                'project_type', 'status'
            )
        }),
        ('Location Details', {
            'fields': (
                'city', 'project_address', 'postal_code',
                'latitude', 'longitude', 'street_map'
            )
        }),
        ('Project Details', {
            'fields': (
                'storeys', 'total_units', 'price_starts',
                'price_end', 'featured_image'
            )
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status and Dates', {
            'fields': (
                'is_featured', 'is_verified',
                'created', 'updated'
            )
        }),
        ('Ownership', {
            'fields': ('user',),
            'classes': ('collapse',)
        })
    )
    
    def price_range(self, obj):
        if obj.price_starts and obj.price_end:
            return f"${obj.price_starts:,.0f} - ${obj.price_end:,.0f}"
        elif obj.price_starts:
            return f"From ${obj.price_starts:,.0f}"
        elif obj.price_end:
            return f"Up to ${obj.price_end:,.0f}"
        return "Price not set"
    price_range.short_description = 'Price Range'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'image_preview', 'title']
    list_filter = ['project']
    search_fields = ['project__project_name', 'title']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'document_type', 'upload_date']
    list_filter = ['document_type', 'upload_date', 'project']
    search_fields = ['title', 'project__project_name']
    readonly_fields = ['upload_date']