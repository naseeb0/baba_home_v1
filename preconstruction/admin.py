from django.contrib import admin
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage

# @admin.register(PreConstruction)
# class PreConstructionAdmin(admin.ModelAdmin):
#     list_display = (
#         'project_name', 'status', 'project_type', 'developer', 'city', 'price_starts', 'price_end'
#     )
#     search_fields = ('project_name', 'description', 'developer__name', 'city__name')
#     list_filter = ('status', 'project_type', 'developer', 'city')
#     prepopulated_fields = {"slug": ("project_name",)}  # Automatically generate slug
#     fieldsets = (
#         (None, {
#             'fields': ('project_name', 'slug', 'storeys', 'total_units', 'price_starts', 'price_end')
#         }),
#         ('Location Details', {
#             'fields': ('project_address', 'postal_code', 'latitude', 'longitude', 'city')
#         }),
#         ('Project Details', {
#             'fields': ('description', 'status', 'project_type', 'street_map', 'developer')
#         }),
#     )
#     readonly_fields = ('slug',)  # Make slug field read-only

# @admin.register(Developer)
# class DeveloperAdmin(admin.ModelAdmin):
#     list_display = ('name', 'website', 'slug')
#     search_fields = ('name', 'website', 'slug')

# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     list_display = ('name', 'city_lat', 'city_long')
#     search_fields = ('name', 'city_lat', 'city_long')

# @admin.register(PreConstructionImage)
# class PreConstructionImageAdmin(admin.ModelAdmin):
#     list_display = ('preconstruction', 'imagealt', 'images')
#     search_fields = ('imagealt', 'preconstruction__project_name')
#     list_filter = ('preconstruction',)


admin.register(City);

admin.site.register(PreConstruction);

admin.site.register(Developer);

admin.site.register(PreConstructionImage);
