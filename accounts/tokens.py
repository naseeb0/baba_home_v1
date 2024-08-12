from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
User = get_user_model()

def create_jwt_pair_for_user(user: AbstractBaseUser):
    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return tokens

#decode JWT


def decode_jwt(access_token_str: str):
    try:
        # Decode the token
        access_token = AccessToken(access_token_str)
        
        # Access token payload
        payload = {
            'user_id': access_token['user_id'],
            'exp': access_token['exp'],
            'iat': access_token['iat']
        }
        return payload
    except (InvalidToken, TokenError) as e:
        # Handle exceptions related to token validity
        return {"error": str(e)}