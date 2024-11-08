from rest_framework.response import Response
from rest_framework.decorators import api_view
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage,PreConstructionFloorPlans, BlogPost
from preconstruction.api.serializers import PreConstructionSerializer, DeveloperSerializer, CitySerializer, BlogPostSerializer
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from preconstruction.api.filters import PreConstructionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from preconstruction.api.pagination import PreconstructionPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class preconstruction_list(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = PreConstructionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    filterset_class = PreConstructionFilter
    search_fields = ['project_name', '=city__name']
    pagination_class = PreconstructionPagination

    def get_queryset(self):
        return PreConstruction.objects.select_related('city', 'developer').all().order_by('id')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        preconstruction = serializer.save(user=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class precon_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_instance = serializer.save()
            
            # Handle new images
            uploaded_images = request.FILES.getlist('uploaded_images')
            for image in uploaded_images:
                PreConstructionImage.objects.create(
                    preconstruction=updated_instance,
                    image=image
                )

            uploaded_floorplans = request.FILES.getlist('uploaded_floorplans')
            for floorplan in uploaded_floorplans:
                PreConstructionFloorPlans.objects.create(
                    preconstruction=updated_instance,
                    floorplan=floorplan
                )
            
            return Response(self.get_serializer(updated_instance).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class developer_list(generics.ListCreateAPIView):
    permission_classes = [];
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class developer_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [];
    queryset = Developer.objects.all().order_by('id')
    serializer_class = DeveloperSerializer

class city_list(generics.ListCreateAPIView):
    permission_classes = [];
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer

class city_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [];
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer


class PreConstructionImageDeleteView(generics.DestroyAPIView):
    queryset = PreConstructionImage.objects.all()
    permission_classes = []

    def delete(self, request, *args, **kwargs):
        image = self.get_object()

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PreconstructionFloorPlanDeleteView(generics.DestroyAPIView):
    queryset = PreConstructionFloorPlans.objects.all()
    permission_classes = []

    def delete(self, request, *args, **kwargs):
        floorplan = self.get_object()

        floorplan.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BlogPostListCreate(generics.ListCreateAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = []
    def get_queryset(self):
        queryset = BlogPost.objects.all()
        
        # Filter by featured
        is_featured = self.request.query_params.get('featured', None)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
            
        # Search by title or content
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
            
        return queryset.order_by('-created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = []
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)