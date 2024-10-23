from rest_framework import serializers
from vacationprojects.models import Builder, Country, City, Project, ProjectImage, ProjectDocument
from vacationprojects.models import BlogPost, BlogCategory, Country, City
from django.contrib.auth import get_user_model

class BuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = ['id', 'name', 'website', 'details', 'slug']

class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_lat', 'country_long']

class CityListSerializer(serializers.ModelSerializer):
    country = CountryListSerializer(read_only=True)
    
    class Meta:
        model = City
        fields = ['id', 'name', 'city_lat', 'city_long', 'country']

class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'image_url', 'title']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

class ProjectDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectDocument
        fields = ['id', 'file', 'file_url', 'title', 'document_type', 'upload_date']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None

class ProjectListSerializer(serializers.ModelSerializer):
    builder = BuilderSerializer(read_only=True)
    city = CityListSerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    images = ProjectImageSerializer(many=True, read_only=True)
    documents = ProjectDocumentSerializer(many=True, read_only=True)
    total_images = serializers.SerializerMethodField()
    total_documents = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'slug', 'meta_title', 'meta_description',
            'price_starts', 'price_end', 'project_type', 'status',
            'featured_image', 'featured_image_url', 'project_address',
            'postal_code', 'latitude', 'longitude',
            'builder', 'city', 'created', 'updated',
            'is_featured', 'is_verified',
            'images', 'documents',
            'total_images', 'total_documents'
        ]
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None
    
    def get_total_images(self, obj):
        return obj.images.count()
    
    def get_total_documents(self, obj):
        return obj.documents.count()

class ProjectDetailSerializer(serializers.ModelSerializer):
    builder = BuilderSerializer(read_only=True)
    city = CityListSerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    images = ProjectImageSerializer(many=True, read_only=True)
    documents = ProjectDocumentSerializer(many=True, read_only=True)
    total_images = serializers.SerializerMethodField()
    total_documents = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'meta_title', 'meta_description',
            'project_name', 'slug', 'storeys', 'total_units',
            'price_starts', 'price_end', 'description',
            'project_address', 'postal_code', 'latitude', 'longitude',
            'status', 'project_type', 'street_map',
            'builder', 'city', 'created', 'updated',
            'featured_image', 'featured_image_url',
            'is_featured', 'is_verified',
            'images', 'documents',
            'total_images', 'total_documents'
        ]
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None
    
    def get_total_images(self, obj):
        return obj.images.count()
    
    def get_total_documents(self, obj):
        return obj.documents.count()

    def create(self, validated_data):
        request = self.context.get('request')
        
        # Handle multiple images
        images = request.FILES.getlist('images', [])
        image_titles = request.POST.getlist('image_titles', [])
        
        # Handle multiple documents
        documents = request.FILES.getlist('documents', [])
        document_titles = request.POST.getlist('document_titles', [])
        document_types = request.POST.getlist('document_types', [])
        
        # Create project
        project = Project.objects.create(**validated_data)
        
        # Create project images
        for i, image in enumerate(images):
            title = image_titles[i] if i < len(image_titles) else ''
            ProjectImage.objects.create(
                project=project,
                image=image,
                title=title
            )
        
        # Create project documents
        for i, document in enumerate(documents):
            title = document_titles[i] if i < len(document_titles) else document.name
            doc_type = document_types[i] if i < len(document_types) else ''
            ProjectDocument.objects.create(
                project=project,
                file=document,
                title=title,
                document_type=doc_type
            )
        
        return project
    
class BlogAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description']

class CountryBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_lat', 'country_long']

class CityBlogSerializer(serializers.ModelSerializer):
    country = CountryBlogSerializer(read_only=True)
    
    class Meta:
        model = City
        fields = ['id', 'name', 'city_lat', 'city_long', 'country']

class BlogListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    author = BlogAuthorSerializer(read_only=True)
    categories = BlogCategorySerializer(many=True, read_only=True)
    countries = CountryBlogSerializer(many=True, read_only=True)
    cities = CityBlogSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'meta_title', 'meta_description',
            'thumbnail', 'thumbnail_url', 'excerpt', 'author',
            'categories', 'countries', 'cities', 'created_at',
            'is_featured', 'views_count'
        ]
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
        return None

class BlogDetailSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    author = BlogAuthorSerializer(read_only=True)
    categories = BlogCategorySerializer(many=True, read_only=True)
    countries = CountryBlogSerializer(many=True, read_only=True)
    cities = CityBlogSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'meta_title', 'meta_description',
            'thumbnail', 'thumbnail_url', 'content', 'excerpt',
            'author', 'categories', 'countries', 'cities',
            'created_at', 'updated_at', 'is_featured', 
            'is_published', 'views_count'
        ]
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
        return None
        
    def create(self, validated_data):
        categories_data = self.context['request'].data.getlist('categories', [])
        countries_data = self.context['request'].data.getlist('countries', [])
        cities_data = self.context['request'].data.getlist('cities', [])
        
        blog_post = BlogPost.objects.create(**validated_data)
        
        # Add categories
        if categories_data:
            blog_post.categories.set(categories_data)
            
        # Add countries
        if countries_data:
            blog_post.countries.set(countries_data)
            
        # Add cities
        if cities_data:
            blog_post.cities.set(cities_data)
            
        return blog_post