from django.urls import path, include
from preconstruction.api.views import preconstruction_list,PreConstructionImageDeleteView, developer_list, precon_details, developer_details, city_list, city_details
urlpatterns = [
    path('preconstruction/', preconstruction_list.as_view(), name='preconstruction-list'),
    path('preconstruction/<int:pk>/', precon_details.as_view(), name='preconstruction-details'),
    path('developer', developer_list.as_view(), name='developer-list'),
    path('developer/<int:pk>/', developer_details.as_view(), name='developer-details'),
    path('city/', city_list.as_view(), name='city-list'),
    path('city/<int:pk>/', city_details.as_view(), name='city-details'),
    path('preconstruction-images/<int:pk>/', PreConstructionImageDeleteView.as_view(), name='preconstruction-image-delete'),


]
