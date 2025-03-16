from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"assets", views.AssetViewSet, basename="assets")
router.register(r"asset-balances", views.AssetBalanceViewSet, basename="asset-balances")

urlpatterns = [
    path("", include(router.urls)),
]
