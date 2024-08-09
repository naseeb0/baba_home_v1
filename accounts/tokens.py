from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model

User = get_user_model()

def create_jwt_pair_for_user(user: AbstractBaseUser):
    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return tokens
