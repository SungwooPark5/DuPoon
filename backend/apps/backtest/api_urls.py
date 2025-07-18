from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r"backtest-results", views.BacktestResultViewSet, basename="backtest-results"
)

urlpatterns = [
    path(
        "static-allocation/",
        views.BacktestAPIView.as_view(),
        name="static_allocation_backtest",
    ),
    path("", include(router.urls)),
]
