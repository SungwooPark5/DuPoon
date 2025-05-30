from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("price/fetch/", views.PriceFetchAPIView.as_view(), name="price_fetch"),
]
