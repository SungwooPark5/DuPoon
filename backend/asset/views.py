from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .models import Asset
from .serializers import AssetSerializer


# Create your views here.
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssetSerializer
