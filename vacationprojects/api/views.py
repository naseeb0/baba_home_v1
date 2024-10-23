from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from vacationprojects.models import Builder, Country, City, Project, ProjectImage, ProjectDocument
from .serializers import (
    BuilderSerializer, CountryListSerializer, CityListSerializer,
    ProjectListSerializer, ProjectDetailSerializer,
    ProjectImageSerializer, ProjectDocumentSerializer
)
from .permissions import IsOwnerOrReadOnly
from .filters import ProjectFilter

class BuilderListCreateView(generics.ListCreateAPIView):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class BuilderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class CountryListCreateView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['country']

class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.prefetch_related(
        'builder', 'city', 'city__country',
        'images', 'documents'
    ).all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['project_name', 'description', 'project_address']
    ordering_fields = ['created', 'price_starts', 'price_end']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectDetailSerializer
        return ProjectListSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.prefetch_related(
        'builder', 'city', 'city__country',
        'images', 'documents'
    ).all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ProjectImageCreateView(generics.CreateAPIView):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)

class ProjectDocumentCreateView(generics.CreateAPIView):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)