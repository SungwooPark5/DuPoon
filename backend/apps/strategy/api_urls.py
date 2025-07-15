from django.urls import path

from .views import StrategyListCreateAPIView

app_name = "strategy"

urlpatterns = [
    path("", StrategyListCreateAPIView.as_view(), name="strategy-list-create"),
]
