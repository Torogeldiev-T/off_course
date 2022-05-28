from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
