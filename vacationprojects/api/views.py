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
from .filters import BlogPostFilter
from .permissions import IsOwnerOrReadOnly
from .filters import ProjectFilter
from .serializers import (
    BlogListSerializer, BlogDetailSerializer,
    BlogCategorySerializer
)
from vacationprojects.models import BlogPost, BlogCategory
from .pagination import BlogPostPagination
from .utils import count_reading_time
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
    
class BlogCategoryListCreateView(generics.ListCreateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class BlogCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.select_related(
        'author'
    ).prefetch_related(
        'categories',
        'countries',
        'cities',
        'cities__country'
    ).filter(is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'views_count']
    pagination_class = BlogPostPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogDetailSerializer
        return BlogListSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.select_related(
        'author'
    ).prefetch_related(
        'categories',
        'countries',
        'cities',
        'cities__country'
    )
    serializer_class = BlogDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        
        # Get related posts
        related_posts = BlogPost.objects.filter(
            is_published=True,
            categories__in=instance.categories.all()
        ).exclude(
            id=instance.id
        ).distinct()[:3]
        
        serializer = self.get_serializer(instance)
        related_serializer = BlogListSerializer(
            related_posts, 
            many=True,
            context={'request': request}
        )
        
        data = serializer.data
        data['related_posts'] = related_serializer.data
        return Response(data)

class RelatedPostsByLocationView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BlogPostPagination

    def get_queryset(self):
        blog_post = BlogPost.objects.get(slug=self.kwargs['slug'])
        return BlogPost.objects.filter(
            is_published=True,
            countries__in=blog_post.countries.all()
        ).exclude(
            id=blog_post.id
        ).distinct()[:3]

class LocationBasedBlogPostsView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BlogPostPagination
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        country_id = self.request.query_params.get('country', None)
        city_id = self.request.query_params.get('city', None)
        
        if country_id:
            queryset = queryset.filter(countries__id=country_id)
        if city_id:
            queryset = queryset.filter(cities__id=city_id)
            
        return queryset.select_related(
            'author'
        ).prefetch_related(
            'categories',
            'countries',
            'cities',
            'cities__country'
        )

class FeaturedBlogPostsView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(
        is_featured=True,
        is_published=True
    ).select_related(
        'author'
    ).prefetch_related(
        'categories',
        'countries',
        'cities',
        'cities__country'
    )
    serializer_class = BlogListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BlogPostPagination