from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from django_filters.rest_framework import DjangoFilterBackend

from .models import Asset, AssetBalance
from .serializers import AssetSerializer, AssetBalanceSerializer


# Create your views here.
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssetSerializer

class AssetBalanceViewSet(viewsets.ModelViewSet):
    queryset = AssetBalance.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssetBalanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["asset", "year", "month"]