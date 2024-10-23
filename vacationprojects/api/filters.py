import django_filters
from vacationprojects.models import Project
from vacationprojects.models import BlogPost

class ProjectFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price_starts', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price_end', lookup_expr='lte')
    project_type = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.CharFilter(lookup_expr='iexact')
    city = django_filters.NumberFilter(field_name='city__id')
    country = django_filters.NumberFilter(field_name='city__country__id')
    builder = django_filters.NumberFilter(field_name='builder__id')
    is_featured = django_filters.BooleanFilter()
    is_verified = django_filters.BooleanFilter()
    created_after = django_filters.DateTimeFilter(field_name='created', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Project
        fields = ['price_min', 'price_max', 'project_type', 'status', 'city', 
                 'country', 'builder', 'is_featured', 'is_verified']

class BlogPostFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='categories__id')
    country = django_filters.NumberFilter(field_name='countries__id')
    city = django_filters.NumberFilter(field_name='cities__id')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = BlogPost
        fields = ['category', 'country', 'city', 'is_featured']