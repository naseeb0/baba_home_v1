from rest_framework.response import Response
from rest_framework.decorators import api_view
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage
from preconstruction.api.serializers import PreConstructionSerializer, DeveloperSerializer, CitySerializer
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated
class preconstruction_list(generics.ListCreateAPIView):
    permission_classes=[];
    queryset = PreConstruction.objects.all().order_by('id')
    serializer_class = PreConstructionSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        preconstruction = serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class precon_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = PreConstruction.objects.all().order_by('id')
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