from django_filters import rest_framework as filters
from preconstruction.models import PreConstruction

class PreConstructionFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price_starts", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="price_starts", lookup_expr='lte')

    class Meta:
        model = PreConstruction
        fields = ['city__name', 'developer__name', 'status', 'project_type', 'user', 'price_min', 'price_max']
