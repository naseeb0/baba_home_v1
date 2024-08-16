from rest_framework.response import Response
from rest_framework.decorators import api_view
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage
from preconstruction.api.serializers import PreConstructionSerializer, DeveloperSerializer, CitySerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
class preconstruction_list(generics.ListCreateAPIView):
    permission_classes=[];
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer

    def post(self, request, *args, **kwargs):
        # Handle image files and other form data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        preconstruction = serializer.save()

        # Handle image files
        image_files = request.FILES.getlist('images')
        for image_file in image_files:
            PreConstructionImage.objects.create(
                preconstruction=preconstruction,
                images=image_file,
                imagealt=request.data.get('imagealt', '')  # Adjust as necessary if `imagealt` is included
            )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class precon_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [];
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer

class developer_list(generics.ListCreateAPIView):
    permission_classes = [];
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class developer_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [];
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class city_list(generics.ListCreateAPIView):
    permission_classes = [];
    queryset = City.objects.all()
    serializer_class = CitySerializer

class city_details(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [];
    queryset = City.objects.all()
    serializer_class = CitySerializer


class PreConstructionImageDeleteView(generics.DestroyAPIView):
    queryset = PreConstructionImage.objects.all()
    permission_classes = []

    def delete(self, request, *args, **kwargs):
        image = self.get_object()

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)