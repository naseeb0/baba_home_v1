from rest_framework import serializers
from preconstruction.models import PreConstruction, Developer,City,PreConstructionImage




class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class PreConstructionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreConstructionImage
        fields = "__all__"

class DeveloperSerializer(serializers.ModelSerializer): 
    # preconstructions = PreConstructionSerializer(many=True, read_only=True)
    class Meta:
        model = Developer
        fields = "__all__"


class PreConstructionSerializer(serializers.ModelSerializer):
    images = PreConstructionImageSerializer(many=True, required=False)
    developer = serializers.PrimaryKeyRelatedField(queryset=Developer.objects.all(), required=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=True)

    class Meta:
        model = PreConstruction
        fields = "__all__"

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        developer = validated_data.pop('developer', None)
        city = validated_data.pop('city', None)

        if not developer or not city:
            raise serializers.ValidationError("Developer and City are required.")

        preconstruction = PreConstruction.objects.create(developer=developer, city=city, **validated_data)

        for image_data in images_data:
            PreConstructionImage.objects.create(preconstructionImage=preconstruction, **image_data)

        return preconstruction