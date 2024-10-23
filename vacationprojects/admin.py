from unfold.admin import ModelAdmin
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, BlogCategory
from .forms import BlogPostAdminForm

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
class BuilderAdmin(ModelAdmin):
    list_display = ['name', 'website', 'slug']
    search_fields = ['name', 'website']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ['name', 'country_lat', 'country_long', 'city_count']
    search_fields = ['name']
    inlines = [CityInline]
    
    def city_count(self, obj):
        return obj.cities.count()
    city_count.short_description = 'Number of Cities'

@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ['name', 'country', 'city_lat', 'city_long']
    list_filter = ['country']
    search_fields = ['name', 'country__name']
    autocomplete_fields = ['country']

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
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
class ProjectImageAdmin(ModelAdmin):
    list_display = ['project', 'image_preview', 'title']
    list_filter = ['project']
    search_fields = ['project__project_name', 'title']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(ModelAdmin):
    list_display = ['title', 'project', 'document_type', 'upload_date']
    list_filter = ['document_type', 'upload_date', 'project']
    search_fields = ['title', 'project__project_name']
    readonly_fields = ['upload_date']

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):  # Note: Using Unfold's ModelAdmin
    form = BlogPostAdminForm
    list_display = [
        'title', 'thumbnail_preview', 'author',
        'created_at', 'is_featured', 'is_published',
        'views_count'
    ]
    list_filter = [
        'is_featured', 'is_published',
        'categories', 'countries', 'cities',
        'created_at'
    ]
    search_fields = ['title', 'content', 'meta_title']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories', 'countries', 'cities']
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'thumbnail_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'author',
                'thumbnail', 'thumbnail_preview',
            )
        }),
        ('Content', {
            'fields': ('content', 'excerpt'),
            'description': 'Use the rich text editor below to format your content. You can upload images directly by dragging and dropping them into the editor.',
            'classes': ('wide',)  # Important for Unfold
        }),
        ('Categories and Locations', {
            'fields': ('categories', 'countries', 'cities'),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': (
                'is_featured', 'is_published',
                'views_count', 'created_at', 'updated_at'
            )
        })
    )
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 4px;"/>', obj.thumbnail.url)
        return "No Thumbnail"
    thumbnail_preview.short_description = 'Preview'
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': [
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            ]
        }
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/js/all.min.js',
        ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['content'].widget.attrs.update({
            'style': 'width: 100%; min-height: 500px;'
        })
        return form