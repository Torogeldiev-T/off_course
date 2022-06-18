from django.shortcuts import render
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .serializers import RegisterSerializer, EmailTokenObtainSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views as jwt_views


class EmailTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
