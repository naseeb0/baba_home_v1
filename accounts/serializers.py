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

    class Meta:
        model = User
        fields = ["email", "username", "password", "company", "phone", "address"]
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
    