from django.contrib.auth.models import User
from rest_framework.views import APIView, Response
from api.serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

