from django.urls import path
from vacationprojects.api.views import (
    BuilderListCreateView, BuilderDetailView,
    CountryListCreateView, CountryDetailView,
    CityListCreateView, CityDetailView,
    ProjectListCreateView, ProjectDetailView,
    ProjectImageCreateView, ProjectDocumentCreateView,
)

app_name = 'vacationprojects'

urlpatterns = [
    # Builder URLs
    path('builders/', BuilderListCreateView.as_view(), name='builder-list'),
    path('builders/<slug:slug>/', BuilderDetailView.as_view(), name='builder-detail'),
    
    # Country URLs
    path('countries/', CountryListCreateView.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
    
    # City URLs
    path('cities/', CityListCreateView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetailView.as_view(), name='city-detail'),
    
    # Project URLs
    path('projects/', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project-detail'),
    
    # Project Images and Documents
    path('projects/<int:project_pk>/images/', ProjectImageCreateView.as_view(), name='project-image-create'),
    path('projects/<int:project_pk>/documents/', ProjectDocumentCreateView.as_view(), name='project-document-create'),
]