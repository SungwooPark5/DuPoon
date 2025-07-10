from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path(
        "static-allocation/",
        views.BacktestAPIView.as_view(),
        name="static_allocation_backtest",
    ),
]
