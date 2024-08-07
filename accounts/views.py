from django.shortcuts import render
from .serializers import SignUpSerializer,LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request


# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response={
                "message":"User created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response={
                "message":"Login successful",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

    def get(self, request: Request):
        content = {"user":str(request.user), "auth":str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)
    