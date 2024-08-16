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
        fields = "__all__"


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'name', 'website', 'details', 'slug']
        extra_kwargs = {
            'slug': {'required': False},
            'id': {'required': False},
        }


class PreConstructionSerializer(serializers.ModelSerializer):
    images = PreConstructionImageSerializer(many=True, required=False)
    developer = DeveloperSerializer()
    city = CitySerializer()

    class Meta:
        model = PreConstruction
        fields = [
            'id', 'meta_title', 'meta_description', 'project_name', 'slug', 'storeys', 'total_units',
            'price_starts', 'price_end', 'description', 'project_address', 'postal_code', 'latitude',
            'longitude', 'occupancy', 'status', 'project_type', 'street_map', 'developer', 'city', 'images'
        ]
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
        }

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
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

        PreConstructionImage.objects.bulk_create([
            PreConstructionImage(preconstructionImage=preconstruction, **image_data)
            for image_data in images_data
        ])

        return preconstruction

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        developer_data = validated_data.pop('developer', None)
        city_data = validated_data.pop('city', None)

        if developer_data:
            developer, _ = Developer.objects.update_or_create(
                id=instance.developer.id,
                defaults=developer_data
            )
            instance.developer = developer

        if city_data:
            city, _ = City.objects.update_or_create(
                id=instance.city.id,
                defaults=city_data
            )
            instance.city = city

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if images_data:
            PreConstructionImage.objects.filter(preconstructionImage=instance).delete()
            PreConstructionImage.objects.bulk_create([
                PreConstructionImage(preconstructionImage=instance, **image_data)
                for image_data in images_data
            ])

        return instance