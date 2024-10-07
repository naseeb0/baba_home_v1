from rest_framework import serializers
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage,PreConstructionFloorPlans

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'city_lat', 'city_long', 'city_details']
        extra_kwargs = {
            'city_lat': {'required': False},
            'city_long': {'required': False},
            'id': {'required': False},
        }

class PreConstructionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreConstructionImage
        fields = ["id", "preconstruction", "image"]

class PreConstructionFloorplanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreConstructionFloorPlans
        fields = ["id", "preconstruction", "floorplan"]

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'name', 'website', 'details', 'slug']
        extra_kwargs = {
            'slug': {'required': False},
            'id': {'required': False},
        }

class PreConstructionSerializer(serializers.ModelSerializer):
    images = PreConstructionImageSerializer(many=True, read_only=True)
    floorplans = PreConstructionFloorplanSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    uploaded_floorplans = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    developer = serializers.PrimaryKeyRelatedField(queryset=Developer.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    city_name = serializers.CharField(source='city.name', read_only=True)
    developer_name = serializers.CharField(source='developer.name', read_only=True)

    class Meta:
        model = PreConstruction
        fields = [
            'id', 'created', 'meta_title', 'meta_description', 'project_name', 'slug', 'storeys', 'total_units',
            'price_starts', 'price_end', 'description', 'project_address', 'postal_code', 'latitude',
            'longitude', 'occupancy', 'status', 'project_type', 'street_map', 'developer', 'developer_name',
            'city', 'city_name', 'images', "uploaded_images", 'user', 'is_featured', 'is_verified','floorplans',
            'uploaded_floorplans'
        ]
        read_only_fields = ['user']

        extra_kwargs = {
            'latitude': {'required': False},
            'longitude': {'required': False},
            'images': {'required': False},
            'floorplans': {'required': False},
            'slug': {'required': False},
            'occupancy': {'required': False},
            'total_units': {'required': False},
            'price_starts': {'required': False},
            'price_end': {'required': False},
            'description': {'required': False},
            'project_address': {'required': False},
            'postal_code': {'required': False},
            'street_map': {'required': False},
            'storeys': {'required': False},
            'meta_title': {'required': False},
            'meta_description': {'required': False},
            'project_type': {'required': True},
            'status': {'required': True},
            'is_featured': {'required': False},
            'is_verified': {'required': False},
        }

    def get_city_name(self, obj):
        return obj.city.name if obj.city else None

    def get_developer_name(self, obj):
        return obj.developer.name if obj.developer else None

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        uploaded_floorplans = validated_data.pop("uploaded_floorplans", [])
        preconstruction = PreConstruction.objects.create(**validated_data)

        for image in uploaded_images:
            PreConstructionImage.objects.create(
                preconstruction=preconstruction,
                image=image,
            )
        for floorplan in uploaded_floorplans:
            PreConstructionFloorPlans.objects.create(
                preconstruction=preconstruction,
                floorplan=floorplan,
            )
        return preconstruction
    
    def update(self, instance, validated_data):
        if 'developer' in validated_data:
            instance.developer = validated_data.pop('developer')

         # Handle city field
        if 'city' in validated_data:
            instance.city = validated_data.pop('city')

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance