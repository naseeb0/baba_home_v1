from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=128, write_only=True)
    company = serializers.CharField(max_length=45, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=45, required=False, allow_blank=True)
    address = serializers.CharField(max_length=45, required=False, allow_blank=True)
    role = serializers.CharField(max_length=45, required=False, allow_blank=False)
    class Meta:
        model = User
        fields = ["email", "username", "password", "company", "phone", "address","role", "id"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def validate(self, attrs):
        email_exits = User.objects.filter(email=attrs["email"]).exists()
        if email_exits:
            raise ValidationError("Email already exists")
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if not user.check_password(password):
                    raise ValidationError("Incorrect password")
            else:
                raise ValidationError("User not found")
        else:
            raise ValidationError("Email and password are required")
        return attrs
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Include any fields you need

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'company', 'phone', 'address']
        extra_kwargs = {
            'username': {'required': False},
            'company': {'required': False},
            'phone': {'required': False},
            'address': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.company = validated_data.get('company', instance.company)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance