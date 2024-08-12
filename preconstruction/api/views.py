from rest_framework.response import Response
from rest_framework.decorators import api_view
from preconstruction.models import PreConstruction, Developer, City
from preconstruction.api.serializers import PreConstructionSerializer, DeveloperSerializer, CitySerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
class preconstruction_list(generics.ListCreateAPIView):
    permission_classes=[];
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer

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
