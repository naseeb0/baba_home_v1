#AUTH TOKEN COMPLETED 
from django.shortcuts import render
from .serializers import SignUpSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            # Retrieve the token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)
            response = {
                "message": "Login Successful",
                "token": token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)
