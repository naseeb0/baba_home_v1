from rest_framework.response import Response
from rest_framework.decorators import api_view
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage,PreConstructionFloorPlans, BlogPost, FloorPlan
from preconstruction.api.serializers import PreConstructionSerializer, DeveloperSerializer, CitySerializer, BlogPostSerializer, FloorPlanSerializer
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


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

class precon_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Get floor plans to delete if any
        floor_plans_to_delete = request.data.getlist('delete_floor_plans', [])
        
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
            
            # Handle new floor plans with categories
            uploaded_floor_plans = request.FILES.items()
            for field_name, image in uploaded_floor_plans:
                if field_name.startswith('floor_plan_'):
                    category = field_name.replace('floor_plan_', '').upper()
                    FloorPlan.objects.create(
                        preconstruction=updated_instance,
                        category=category,
                        image=image,
                        name=f"{updated_instance.project_name} - {category}"
                    )
            
            # Delete floor plans if requested
            if floor_plans_to_delete:
                FloorPlan.objects.filter(
                    id__in=floor_plans_to_delete,
                    preconstruction=updated_instance
                ).delete()
            
            return Response(self.get_serializer(updated_instance).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class FloorPlanOperations(generics.GenericAPIView):
    permission_classes = []
    queryset = PreConstruction.objects.all()

    def post(self, request, pk):
        action_type = request.data.get('action_type')
        preconstruction = self.get_object()

        if action_type == 'delete_specific':
            floor_plan_ids = request.data.getlist('floor_plan_ids', [])
            if floor_plan_ids:
                deleted_count = FloorPlan.objects.filter(
                    id__in=floor_plan_ids,
                    preconstruction=preconstruction
                ).delete()[0]
                
                return Response({
                    'message': f'Successfully deleted {deleted_count} floor plans',
                    'deleted_count': deleted_count
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'No floor plan IDs provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        elif action_type == 'delete_all':
            deleted_count = preconstruction.floor_plan_images.all().delete()[0]
            return Response({
                'message': f'Successfully deleted all {deleted_count} floor plans',
                'deleted_count': deleted_count
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Invalid action_type'
        }, status=status.HTTP_400_BAD_REQUEST) 
    
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