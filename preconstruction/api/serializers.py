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
    developer = serializers.PrimaryKeyRelatedField(queryset=Developer.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = PreConstruction
        fields = "__all__"

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        developer_data = validated_data.pop('developer', None)
        city_data = validated_data.pop('city', None)

        if developer_data:
            developer, _ = Developer.objects.get_or_create(**developer_data)
            validated_data['developer'] = developer

        if city_data:
            city, _ = City.objects.get_or_create(**city_data)
            validated_data['city'] = city

        preconstruction = PreConstruction.objects.create(**validated_data)

        for image_data in images_data:
            PreConstructionImage.objects.create(preconstructionImage=preconstruction, **image_data)

        return preconstruction
