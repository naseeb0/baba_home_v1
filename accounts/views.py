#JWT COMPLeted
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from django.conf import settings

from .serializers import SignUpSerializer, LoginSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .tokens import create_jwt_pair_for_user, decode_jwt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
User = get_user_model()
import logging


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            new_user = serializer.save()
            if new_user:
                access_token = create_jwt_pair_for_user(new_user)
                data = {'access_token':access_token}
                response = Response(data=data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                return response
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = Response({
                "message": "Login Successful",
                "token": tokens
            }, status = status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=tokens['access'], httponly=True, samesite='Lax')
            return response
        else:
            return Response(data={"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)

#Creating User Logout LogoutView

class LogoutView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

#To check user authentication status, you can use the following view: JWT Authentication .. Use Browser JWT access_token from cookie
logger = logging.getLogger(__name__)

class UserViewAPI(generics.GenericAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
		user_token = request.COOKIES.get('access_token')

		if not user_token:
			raise Exception('Unauthenticated user.')

		payload = decode_jwt(user_token)

		user_model = get_user_model()
		user = user_model.objects.filter(id=payload['user_id']).first()
		user_serializer = SignUpSerializer(user)
		return Response(user_serializer.data)