from rest_framework.response import Response
from rest_framework.decorators import api_view
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage,PreConstructionFloorPlans, BlogPost, FloorPlan, Feature, SampleAPS, Siteplan, FloorPlanDocs
from preconstruction.api.serializers import PreConstructionSerializer, DeveloperSerializer, CitySerializer, BlogPostSerializer, FloorPlanSerializer, FeatureSerializer, SampleAPSSerializer, SiteplanSerializer, FloorPlanDocsSerializer
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from preconstruction.api.filters import PreConstructionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import os
from rest_framework.permissions import IsAuthenticated, AllowAny
from preconstruction.api.pagination import PreconstructionPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

@method_decorator(csrf_exempt, name='dispatch')
class preconstruction_list(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating preconstruction projects.
    
    get:
    Return a list of all preconstruction projects, with optional filtering and search.
    
    post:
    Create a new preconstruction project.
    """
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


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

class precon_details(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific preconstruction project.
    
    get:
    Return details of a specific preconstruction project.
    
    patch:
    Partially update a preconstruction project, including image and floor plan handling.
    
    put:
    Update a preconstruction project (redirects to patch).
    
    delete:
    Delete a preconstruction project.
    """
    permission_classes = []
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Log received data for debugging
        print("Received data:", request.data)
        print("Received files:", request.FILES)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_instance = serializer.save()
            
            # Handle new images
            images = request.FILES.getlist('images', [])
            for image in images:
                PreConstructionImage.objects.create(
                    preconstruction=updated_instance,
                    image=image
                )
            
            # Handle floor plans
            floor_plan_images = request.FILES.getlist('floor_plan_images', [])
            floor_plan_categories = request.data.getlist('floor_plan_categories', [])
            floor_plan_names = request.data.getlist('floor_plan_names', [])
            floor_plan_square_footages = request.data.getlist('floor_plan_square_footages', [])
            
            # Create floor plans
            for i, image in enumerate(floor_plan_images):
                category = floor_plan_categories[i] if i < len(floor_plan_categories) else 'UNCATEGORIZED'
                name = floor_plan_names[i] if i < len(floor_plan_names) else f"Floor Plan {i+1}"
                square_footage = floor_plan_square_footages[i] if i < len(floor_plan_square_footages) else None
                
                FloorPlan.objects.create(
                    preconstruction=updated_instance,
                    category=category,
                    image=image,
                    name=name,
                    square_footage=square_footage
                )
            
            return Response(self.get_serializer(updated_instance).data, status=status.HTTP_200_OK)
        
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)  # Redirect PUT to PATCH for consistency

class developer_list(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating developers.
    
    get:
    Return a list of all developers.
    
    post:
    Create a new developer.
    """
    permission_classes = [];
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class developer_details(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific developer.
    """
    permission_classes = [];
    queryset = Developer.objects.all().order_by('id')
    serializer_class = DeveloperSerializer

class city_list(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating cities.
    
    get:
    Return a list of all cities.
    
    post:
    Create a new city.
    """
    permission_classes = [];
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer

class city_details(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific city.
    """
    permission_classes = [];
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer


class PreConstructionImageDeleteView(generics.DestroyAPIView):
    """
    API endpoint for deleting preconstruction images.
    Handles both database record and physical file deletion.
    """
    queryset = PreConstructionImage.objects.all()
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        try:
            # Get the ID from kwargs
            image_id = kwargs.get('pk')
            print(f"Attempting to delete image with ID: {image_id}")

            # Get the instance
            instance = PreConstructionImage.objects.get(id=image_id)
            print(f"Found image instance: {instance}")
            print(f"Image path: {instance.image.path if instance.image else 'No image path'}")

            # Store image path before deletion if it exists
            image_path = None
            if instance.image:
                try:
                    image_path = instance.image.path
                    print(f"Image physical path: {image_path}")
                except Exception as e:
                    print(f"Error getting image path: {e}")

            # Delete the database record first
            instance_id = instance.id  # Store ID for response
            instance.delete()
            print(f"Database record deleted for image ID: {instance_id}")

            # Then try to delete the physical file if it exists
            if image_path and os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                    print(f"Physical file deleted: {image_path}")
                except OSError as e:
                    print(f"Error deleting physical file: {e}")
                    # Continue anyway since DB record is already deleted

            return Response({
                "message": "Image deleted successfully",
                "image_id": instance_id
            }, status=status.HTTP_200_OK)

        except PreConstructionImage.DoesNotExist:
            print(f"Image not found with ID: {kwargs.get('pk')}")
            return Response({
                "error": f"Image not found with ID: {kwargs.get('pk')}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error during image deletion: {str(e)}")
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
class PreconstructionFloorPlanDeleteView(generics.DestroyAPIView):
    """
    API endpoint for deleting floor plan images.
    Handles both database record and physical file deletion.
    """
    queryset = FloorPlan.objects.all()
    lookup_field = 'pk'
    permission_classes = [AllowAny]  # or remove this line to allow unauthenticated access

    def delete(self, request, *args, **kwargs):
        try:
            # Get the ID from the lookup field
            floor_plan_id = self.kwargs[self.lookup_field]
            print(f"Attempting to delete floor plan with ID: {floor_plan_id}")

            # Get the instance
            instance = self.get_object()
            
            # Store image path before deletion
            image_path = instance.image.path if instance.image else None
            print(f"Floor plan physical path: {image_path}")

            # Delete database record
            instance_id = instance.id
            instance.delete()
            print(f"Database record deleted for floor plan ID: {instance_id}")

            # Delete physical file if exists
            if image_path and os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                    print(f"Physical file deleted: {image_path}")
                except OSError as e:
                    print(f"Error deleting physical file: {e}")

            return Response({
                "message": "Floor plan deleted successfully",
                "floor_plan_id": instance_id
            }, status=status.HTTP_200_OK)

        except FloorPlan.DoesNotExist:
            print(f"Floor plan not found with ID: {floor_plan_id}")
            return Response({
                "error": f"Floor plan not found with ID: {floor_plan_id}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error during floor plan deletion: {str(e)}")
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
class BlogPostListCreate(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating blog posts.
    
    get:
    Return a list of all blog posts.
    
    post:
    Create a new blog post.
    """
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
    """
    API endpoint for retrieving, updating, and deleting blog posts.
    Uses slug field for lookups instead of primary key.
    """
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

class PreconstructionList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating preconstruction projects.
    
    get:
    Return a list of all preconstruction projects.
    
    post:
    Create a new preconstruction project.
    """
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = PreConstruction.objects.all()
        return queryset

class PreconstructionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a preconstruction project.
    """
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DeveloperList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating developers.
    
    get:
    Return a list of all developers.
    
    post:
    Create a new developer.
    """
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DeveloperDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a developer.
    """
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CityList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating cities.
    
    get:
    Return a list of all cities.
    
    post:
    Create a new city.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a city.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FeatureList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating features.
    Supports filtering by preconstruction_id.
    """
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Feature.objects.all()
        preconstruction_id = self.request.query_params.get('preconstruction', None)
        if preconstruction_id is not None:
            queryset = queryset.filter(preconstruction_id=preconstruction_id)
        return queryset

class FeatureDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting a feature.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SampleAPSList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating sample APS documents.
    Supports filtering by preconstruction_id.
    """
    serializer_class = SampleAPSSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = SampleAPS.objects.all()
        preconstruction_id = self.request.query_params.get('preconstruction', None)
        if preconstruction_id is not None:
            queryset = queryset.filter(preconstruction_id=preconstruction_id)
        return queryset

class SampleAPSDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting a sample APS document.
    """
    queryset = SampleAPS.objects.all()
    serializer_class = SampleAPSSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SiteplanList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating site plans.
    Supports filtering by preconstruction_id.
    """
    serializer_class = SiteplanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Siteplan.objects.all()
        preconstruction_id = self.request.query_params.get('preconstruction', None)
        if preconstruction_id is not None:
            queryset = queryset.filter(preconstruction_id=preconstruction_id)
        return queryset

class SiteplanDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting a site plan.
    """
    queryset = Siteplan.objects.all()
    serializer_class = SiteplanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FloorPlanDocsList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating floor plan documents.
    Supports filtering by preconstruction_id.
    """
    serializer_class = FloorPlanDocsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = FloorPlanDocs.objects.all()
        preconstruction_id = self.request.query_params.get('preconstruction', None)
        if preconstruction_id is not None:
            queryset = queryset.filter(preconstruction_id=preconstruction_id)
        return queryset

class FloorPlanDocsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting a floor plan document.
    """
    queryset = FloorPlanDocs.objects.all()
    serializer_class = FloorPlanDocsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]