from rest_framework import serializers
from preconstruction.models import PreConstruction, Developer,City

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=200)
#     active = serializers.BooleanField(default=True)
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
# class WebSeriesSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=200)
#     country = serializers.CharField(max_length=50)

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)


# class MovieSerializer(serializers.ModelSerializer):
#     len_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Movie
#         # fields = ['id', 'name', 'description']
#         exclude = ['active']
    
#     def get_len_name(self, obj):
#         length = len(obj.name)
#         return length


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