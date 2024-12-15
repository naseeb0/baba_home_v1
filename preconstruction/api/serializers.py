from rest_framework import serializers
from preconstruction.models import PreConstruction, Developer, City, PreConstructionImage,PreConstructionFloorPlans,BlogPost,FloorPlan, Feature, SampleAPS, Siteplan, FloorPlanDocs

class FeatureSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            return f'/media/{obj.file}'
        return None

    class Meta:
        model = Feature
        fields = ['id', 'preconstruction', 'title', 'description', 'file', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class FloorPlanDocsSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            return f'/media/{obj.file}'
        return None

    class Meta:
        model = FloorPlanDocs
        fields = ['id', 'preconstruction', 'title', 'description', 'file', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SampleAPSSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            return f'/media/{obj.file}'
        return None

    class Meta:
        model = SampleAPS
        fields = ['id', 'preconstruction', 'title', 'description', 'file', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SiteplanSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            return f'/media/{obj.file}'
        return None

    class Meta:
        model = Siteplan
        fields = ['id', 'preconstruction', 'title', 'description', 'file', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PreConstructionImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return f'/media/{obj.image}'
        return None

    class Meta:
        model = PreConstructionImage
        fields = ["id", "preconstruction", "image"]

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'city_lat', 'city_long', 'city_details']
        extra_kwargs = {
            'city_lat': {'required': False},
            'city_long': {'required': False},
            'id': {'required': False},
        }

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'name', 'website', 'details', 'slug', 'sales_office_address', 'email', 'phone', 'commission', 'sales_person_name', 'sales_person_contact']
        extra_kwargs = {
            'slug': {'required': False},
            'id': {'required': False},
            'sales_office_address': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'commission': {'required': False},
            'sales_person_name': {'required': False},
            'sales_person_contact': {'required': False},
        }

class FloorPlanSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return f'/media/{obj.image}'
        return None

    class Meta:
        model = FloorPlan
        fields = ['id', 'preconstruction', 'category', 'image', 'image_url', 'name', 'square_footage', 'price', 'created']

class PreConstructionSerializer(serializers.ModelSerializer):
    images = PreConstructionImageSerializer(many=True, read_only=True)
    floor_plan_images = FloorPlanSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    floorplan_docs = FloorPlanDocsSerializer(many=True, read_only=True)
    sample_aps = SampleAPSSerializer(many=True, read_only=True)
    siteplans = SiteplanSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    uploaded_floor_plans = serializers.DictField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    developer = serializers.PrimaryKeyRelatedField(queryset=Developer.objects.all())
    developer_details = DeveloperSerializer(source='developer', read_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    city_name = serializers.CharField(source='city.name', read_only=True)
    developer_name = serializers.CharField(source='developer.name', read_only=True)

    class Meta:
        model = PreConstruction
        fields = [
            'id', 'created', 'meta_title', 'meta_description', 'project_name', 'slug', 'storeys', 'total_units',
            'price_starts', 'price_end', 'description', 'deposit_structure', 'incentives', 'project_completion', 'project_address', 
            'postal_code', 'latitude', 'longitude', 'occupancy', 'status', 'project_type', 'street_map', 
            'developer', 'developer_name', 'developer_details', 'city', 'city_name', 
            'images', 'uploaded_images', 'floor_plan_images', 'uploaded_floor_plans',
            'features', 'floorplan_docs', 'sample_aps', 'siteplans',
            'user', 'is_featured', 'is_verified'
        ]
        read_only_fields = ['user']

        extra_kwargs = {
            'latitude': {'required': False},
            'longitude': {'required': False},
            'images': {'required': False},
            'floor_plan_images': {'required': False},
            'slug': {'required': False},
            'occupancy': {'required': False},
            'total_units': {'required': False},
            'price_starts': {'required': False},
            'price_end': {'required': False},
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
        uploaded_floor_plans = validated_data.pop("uploaded_floor_plans", {})
        preconstruction = PreConstruction.objects.create(**validated_data)

        # Handle regular images
        for image in uploaded_images:
            PreConstructionImage.objects.create(
                preconstruction=preconstruction,
                image=image,
            )
        
        # Handle floor plans
        # Expected format: {"1BED": image1, "2BED": image2, ...}
        for category, image in uploaded_floor_plans.items():
            FloorPlan.objects.create(
                preconstruction=preconstruction,
                category=category,
                image=image,
                name=f"{preconstruction.project_name} - {category}"
            )

        return preconstruction
    
    def update(self, instance, validated_data):
        uploaded_floor_plans = validated_data.pop("uploaded_floor_plans", {})
        
        if 'developer' in validated_data:
            instance.developer = validated_data.pop('developer')

        if 'city' in validated_data:
            instance.city = validated_data.pop('city')

        # Handle new floor plans
        for category, image in uploaded_floor_plans.items():
            FloorPlan.objects.create(
                preconstruction=instance,
                category=category,
                image=image,
                name=f"{instance.project_name} - {category}"
            )

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class BlogPostSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return f'/media/{obj.thumbnail}'
        return None

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'thumbnail',
            'thumbnail_url',  
            'meta_title',
            'meta_description',
            'content',
            'created_at',
            'updated_at',
            'is_featured',
            'views_count'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'thumbnail_url']