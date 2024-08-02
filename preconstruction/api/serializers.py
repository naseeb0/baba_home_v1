from rest_framework import serializers
from preconstruction.models import PreConstruction, Developer,City

class PreConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreConstruction
        fields = "__all__"

class DeveloperSerializer(serializers.ModelSerializer): 
    preconstructions = PreConstructionSerializer(many=True, read_only=True)
    class Meta:
        model = Developer
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"