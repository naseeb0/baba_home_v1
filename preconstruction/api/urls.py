from django.urls import path, include
from preconstruction.api.views import preconstruction_list, developer_list, precon_details, developer_details, city_list, city_details
urlpatterns = [
    path('preconstruction/', preconstruction_list, name='preconstruction-list'),
    path('preconstruction/<int:pk>/', precon_details, name='preconstruction-details'),
    path('developer', developer_list, name='developer-list'),
    path('developer/<int:pk>/', developer_details, name='developer-details'),
    path('city/', city_list, name='city-list'),
    path('city/<int:pk>/', city_details, name='city-details'),
]
