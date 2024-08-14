from rest_framework import serializers
from preconstruction.models import PreConstruction, Developer,City,PreConstructionImage




class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'city_lat', 'city_long', 'city_details']
        extra_kwargs = {'city_lat':{'required':False}, 
                        'city_long':{'required':False}}

class PreConstructionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreConstructionImage
        fields = "__all__"

class DeveloperSerializer(serializers.ModelSerializer): 
    # preconstructions = PreConstructionSerializer(many=True, read_only=True)
    class Meta:
        model = Developer
        fields = ['id', 'name', 'website', 'details', 'slug']
        extra_kwargs = {'slug':{'required':False}}




class PreConstructionSerializer(serializers.ModelSerializer):
    images = PreConstructionImageSerializer(many=True, required=False)
    developer = DeveloperSerializer()  
    city = CitySerializer()  

    class Meta:
        model = PreConstruction
        fields = ['id', 'meta_title', 'meta_description', 'project_name', 'slug', 'storeys', 'total_units', 'price_starts', 'price_end', 'description', 'project_address', 'postal_code', 'latitude', 'longitude', 'occupancy', 'status', 'project_type', 'street_map', 'developer', 'city', 'images']
        extra_kwargs = {'latitude': {'required':False}, 
                        'longitude': {'required':False},
                        'images': {'required':False},
                        'slug': {'required':False},
                        'occupancy': {'required':False},
                        'total_units': {'required':False},
                        'price_starts': {'required':False},
                        'price_end': {'required':False},
                        'description': {'required':False},
                        'project_address': {'required':False},
                        'postal_code': {'required':False},
                        'street_map': {'required':False},
                        'storeys': {'required':False},
                        'meta_title': {'required':False},
                        'meta_description': {'required':False},
                        'project_type': {'required': True},  # Ensures 'project_type' is required
                        'status': {'required': True},        
        }

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        developer_data = validated_data.pop('developer')
        city_data = validated_data.pop('city')

        developer = Developer.objects.get_or_create(**developer_data)[0]
        city = City.objects.get_or_create(**city_data)[0]

        preconstruction = PreConstruction.objects.create(developer=developer, city=city, **validated_data)

        for image_data in images_data:
            PreConstructionImage.objects.create(preconstructionImage=preconstruction, **image_data)

        return preconstruction
