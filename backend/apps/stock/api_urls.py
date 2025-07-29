from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"stocks", views.StockViewSet, basename="stock")

urlpatterns = [
    path("price/fetch/", views.PriceFetchAPIView.as_view(), name="price_fetch"),
    path("", include(router.urls)),
]
