from rest_framework import serializers
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage


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
    uploaded_images = serializers.ListField(
    child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
    write_only=True,
)
    developer = DeveloperSerializer()
    city = CitySerializer()

    class Meta:
        model = PreConstruction
        fields = [
            'id', 'created','meta_title', 'meta_description', 'project_name', 'slug', 'storeys', 'total_units',
            'price_starts', 'price_end', 'description', 'project_address', 'postal_code', 'latitude',
            'longitude', 'occupancy', 'status', 'project_type', 'street_map', 'developer', 'city', 'images', "uploaded_images", 'user',
            'is_featured',
            'is_verified'
        ]
        read_only_fields = ['user']

        extra_kwargs = {
            'latitude': {'required': False},
            'longitude': {'required': False},
            'images': {'required': False},
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
            'uploaded_images': {'required': False},
            'is_featured': {'required': False},
            'is_verified': {'required': False},
        }

    
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        developer_data = validated_data.pop('developer')
        city_data = validated_data.pop('city')

        city, _ = City.objects.get_or_create(
            name=city_data.get('name'),
            defaults=city_data
        )

        developer, _ = Developer.objects.get_or_create(
            name=developer_data.get('name'),
            defaults=developer_data
        )
        preconstruction = PreConstruction.objects.create(developer=developer, city=city, **validated_data)

        for image in uploaded_images:
            PreConstructionImage.objects.create(
                preconstruction=preconstruction,
                image=image,
            )

        return preconstruction
    
    def update(self, instance, validated_data):
        developer_data = validated_data.pop('developer', None)
        if developer_data:
            developer, created = Developer.objects.update_or_create(
                name=developer_data.get('name', instance.developer.name),
                defaults=developer_data
            )
            instance.developer = developer

        city_data = validated_data.pop('city', None)
        if city_data:
            city, created = City.objects.update_or_create(
                name=city_data.get('name', instance.city.name),
                defaults=city_data
            )
            instance.city = city

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance