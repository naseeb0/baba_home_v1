from unfold.admin import ModelAdmin
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.db import models
from preconstruction.models import (
    PreConstruction, Developer, City, PreConstructionImage, 
    PreConstructionFloorPlans, FloorPlan, BlogPost, Feature, SampleAPS, Siteplan, FloorPlanDocs
)
from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField

@admin.register(Developer)
class DeveloperAdmin(ModelAdmin):
    list_display = ('name', 'website', 'email', 'phone', 'sales_person_name', 'commission', 'slug')
    search_fields = ('name', 'details', 'email', 'sales_person_name', 'sales_office_address')
    fields = ('name', 'website', 'details', 'slug', 'sales_office_address', 'email', 
              'phone', 'commission', 'sales_person_name', 'sales_person_contact')
    prepopulated_fields = {'slug': ('name',)}

class PreConstructionImageInline(admin.TabularInline):
    model = PreConstructionImage
    extra = 3
    fields = ('image', 'get_image_preview')  # Removed delete_image
    readonly_fields = ('get_image_preview',)
    can_delete = True  # This enables the deletion checkbox
    show_change_link = True

    def get_image_preview(self, obj):
        if obj and obj.image:
            return mark_safe(f'''
                <img src="{obj.image.url}" style="max-height: 100px;"/>
                <br>
                <input type="checkbox" name="_delete_{obj.id}" id="delete_{obj.id}" class="delete-checkbox">
                <label for="delete_{obj.id}">Mark for deletion</label>
            ''')
        return ""
    get_image_preview.short_description = 'Preview'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('preconstruction')

    def has_delete_permission(self, request, obj=None):
        return True

class FloorPlanForm(forms.ModelForm):
    class Meta:
        model = FloorPlan
        fields = ['category', 'image', 'name', 'square_footage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ChoiceField(
            choices=[
                ("1BED", "1 Bedroom"),
                ("2BED", "2 Bedroom"),
                ("3BED", "3 Bedroom"),
                ("4BED", "4 Bedroom"),
                ("OTHER", "Other")
            ]
        )

class FloorPlanInline(admin.TabularInline):
    model = FloorPlan
    form = FloorPlanForm
    extra = 1
    fields = ['category', 'image', 'get_image_preview', 'name', 'square_footage', 'price']
    readonly_fields = ('get_image_preview',)
    can_delete = True  # Enable deletion for inline
    show_change_link = True

    def get_image_preview(self, obj):
        if obj and obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'''
                <img src="{obj.image.url}" style="max-height: 100px;"/>
                <br>
                <a href="#" onclick="if (confirm('Are you sure you want to delete this floor plan?')) {{
                    fetch('/admin/preconstruction/floorplan/{obj.id}/delete/', {{
                        method: 'POST',
                        headers: {{'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}}
                    }}).then(() => window.location.reload());
                    return false;
                }}">Delete Floor Plan</a>
            ''')
        return ""
    get_image_preview.short_description = 'Preview'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('preconstruction')

    def has_delete_permission(self, request, obj=None):
        return True

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            kwargs['widget'] = forms.ClearableFileInput(attrs={'accept': 'image/*'})
        return super().formfield_for_dbfield(db_field, request, **kwargs)

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1
    fields = ('title', 'file', 'file_preview')
    readonly_fields = ('file_preview',)
    can_delete = True
    show_change_link = True

    def file_preview(self, obj):
        if obj and obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'Preview'

class FloorPlanDocsInline(admin.TabularInline):
    model = FloorPlanDocs
    extra = 1
    fields = ('title', 'file', 'file_preview')
    readonly_fields = ('file_preview',)
    can_delete = True
    show_change_link = True

    def file_preview(self, obj):
        if obj and obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'Preview'

class SampleAPSInline(admin.TabularInline):
    model = SampleAPS
    extra = 1
    fields = ('title', 'file', 'file_preview')
    readonly_fields = ('file_preview',)
    can_delete = True
    show_change_link = True

    def file_preview(self, obj):
        if obj and obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'Preview'

class SiteplanInline(admin.TabularInline):
    model = Siteplan
    extra = 1
    fields = ('title', 'file', 'file_preview')
    readonly_fields = ('file_preview',)
    can_delete = True
    show_change_link = True

    def file_preview(self, obj):
        if obj and obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'Preview'

@admin.register(PreConstruction)
class PreConstructionAdmin(ModelAdmin):
    list_display = ('project_name', 'status', 'project_type', 'developer', 'city', 
                   'is_featured', 'is_verified', 'created', 'main_image_preview')
    list_filter = ('status', 'project_type', 'developer', 'city', 'is_featured', 'is_verified')
    search_fields = ('project_name', 'description', 'project_address', 'postal_code')
    inlines = [PreConstructionImageInline, FloorPlanInline, FeatureInline, FloorPlanDocsInline, SampleAPSInline, SiteplanInline]
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE()},
    }
    fieldsets = (
        ('Meta Information', {
            'fields': ('meta_title', 'meta_description', 'project_name', 'slug')
        }),
        ('Project Details', {
            'fields': (
                'storeys', 'total_units', 'price_starts', 'price_end',
                'description', 'deposit_structure', 'incentives', 'project_completion', 'project_address', 'postal_code',
                'latitude', 'longitude', 'occupancy', 'status',
                'project_type', 'street_map'
            )
        }),
        ('Relationships', {
            'fields': ('developer', 'city', 'user')
        }),
        ('Main Image', {
            'fields': ('image', 'main_image_preview')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_verified')
        })
    )
    readonly_fields = ('main_image_preview',)

    def main_image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;"/>')
        return ""
    main_image_preview.short_description = "Main Image Preview"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        
        # Get the instance after it's been saved
        instance = form.instance
        
        # Handle floor plan formset specifically
        for formset in formsets:
            if isinstance(formset, FloorPlanInline):
                for floor_plan_form in formset.forms:
                    if floor_plan_form.cleaned_data and not floor_plan_form.cleaned_data.get('DELETE', False):
                        # Only process if we have cleaned data and it's not marked for deletion
                        if floor_plan_form.instance.pk is None:  # This is a new floor plan
                            if floor_plan_form.cleaned_data.get('image'):
                                floor_plan = floor_plan_form.save(commit=False)
                                floor_plan.preconstruction = instance
                                floor_plan.save()

@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ('name', 'city_lat', 'city_long')
    search_fields = ('name', 'city_details')
    fields = ('name', 'city_lat', 'city_long', 'city_details')

@admin.register(PreConstructionImage)
class PreConstructionImageAdmin(ModelAdmin):
    list_display = ('preconstruction', 'image_preview', 'delete_action')
    list_filter = ('preconstruction',)
    fields = ('preconstruction', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def delete_action(self, obj):
        if obj.id:
            return mark_safe(f'<a href="/admin/preconstruction/preconstructionimage/{obj.id}/delete/" class="deletelink">Delete</a>')
        return ""
    delete_action.short_description = "Actions"

    def image_preview(self, obj):
        if obj and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 150px;"/>')
        return ""
    image_preview.short_description = "Image Preview"

@admin.register(PreConstructionFloorPlans)
class PreConstructionFloorPlansAdmin(ModelAdmin):
    list_display = ('preconstruction', 'floorplan_preview', 'delete_action')
    list_filter = ('preconstruction',)
    fields = ('preconstruction', 'floorplan', 'floorplan_preview')
    readonly_fields = ('floorplan_preview',)

    def delete_action(self, obj):
        if obj.id:
            return mark_safe(f'<a href="/admin/preconstruction/preconstructionfloorplans/{obj.id}/delete/" class="deletelink">Delete</a>')
        return ""
    delete_action.short_description = "Actions"

    def floorplan_preview(self, obj):
        if obj and obj.floorplan:
            return mark_safe(f'<img src="{obj.floorplan.url}" style="max-height: 150px;"/>')
        return ""
    floorplan_preview.short_description = "Floorplan Preview"

@admin.register(FloorPlan)
class FloorPlanAdmin(ModelAdmin):
    form = FloorPlanForm
    list_display = ('preconstruction', 'category', 'name', 'square_footage', 'image_preview', 'delete_action')
    list_filter = ('category', 'preconstruction')
    search_fields = ['name', 'preconstruction__project_name']
    fields = ('preconstruction', 'category', 'image', 'image_preview', 'name', 'square_footage')
    readonly_fields = ('image_preview',)

    def delete_action(self, obj):
        if obj.id:
            return mark_safe(f'<a href="/admin/preconstruction/floorplan/{obj.id}/delete/" class="deletelink">Delete</a>')
        return ""
    delete_action.short_description = "Actions"

    def image_preview(self, obj):
        if obj and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 150px;"/>')
        return ""
    image_preview.short_description = "Image Preview"

@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_featured', 'views_count', 'thumbnail_preview')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'content', 'meta_title')
    fields = (
        'title', 'slug', 'thumbnail', 'thumbnail_preview',
        'meta_title', 'meta_description',
        'content', 'is_featured', 'views_count'
    )
    readonly_fields = ('created_at', 'updated_at', 'views_count', 'slug', 'thumbnail_preview')

    def thumbnail_preview(self, obj):
        if obj and obj.thumbnail:
            delete_url = ''
            if obj.thumbnail:
                delete_url = f'''
                    <br>
                    <a href="#" onclick="if (confirm('Are you sure you want to delete the thumbnail?')) {{
                        document.getElementById('id_thumbnail').value = '';
                        document.getElementById('id_thumbnail-clear_id').checked = true;
                        return false;
                    }}">Delete Thumbnail</a>
                '''
            return mark_safe(f'<img src="{obj.thumbnail.url}" style="max-height: 150px;"/>{delete_url}')
        return ""
    thumbnail_preview.short_description = "Thumbnail Preview"

@admin.register(Feature)
class FeatureAdmin(ModelAdmin):
    list_display = ('title', 'preconstruction', 'file_preview', 'created_at')
    list_filter = ('preconstruction', 'created_at')
    search_fields = ('title', 'description', 'preconstruction__project_name')
    fields = ('preconstruction', 'title', 'file', 'file_preview')
    readonly_fields = ('file_preview', 'created_at', 'updated_at')

    def file_preview(self, obj):
        if obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'File Preview'

@admin.register(SampleAPS)
class SampleAPSAdmin(ModelAdmin):
    list_display = ('title', 'preconstruction', 'file_preview', 'created_at')
    list_filter = ('preconstruction', 'created_at')
    search_fields = ('title', 'description', 'preconstruction__project_name')
    fields = ('preconstruction', 'title', 'file', 'file_preview')
    readonly_fields = ('file_preview', 'created_at', 'updated_at')

    def file_preview(self, obj):
        if obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'File Preview'

@admin.register(Siteplan)
class SiteplanAdmin(ModelAdmin):
    list_display = ('title', 'preconstruction', 'file_preview', 'created_at')
    list_filter = ('preconstruction', 'created_at')
    search_fields = ('title', 'description', 'preconstruction__project_name')
    fields = ('preconstruction', 'title', 'file', 'file_preview')
    readonly_fields = ('file_preview', 'created_at', 'updated_at')

    def file_preview(self, obj):
        if obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'File Preview'

@admin.register(FloorPlanDocs)
class FloorPlanDocsAdmin(ModelAdmin):
    list_display = ('title', 'preconstruction', 'file_preview', 'created_at')
    list_filter = ('preconstruction', 'created_at')
    search_fields = ('title', 'description', 'preconstruction__project_name')
    fields = ('preconstruction', 'title', 'file', 'file_preview')
    readonly_fields = ('file_preview', 'created_at', 'updated_at')

    def file_preview(self, obj):
        if obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'svg']:
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px;"/>')
            elif file_extension == 'pdf':
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">View PDF</a>')
            else:
                return mark_safe(f'<a href="{obj.file.url}" target="_blank" class="button">Download File</a>')
        return ""
    file_preview.short_description = 'File Preview'