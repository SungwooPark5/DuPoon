from django.urls import path

from .views import StrategyView, StrategyListView, StrategyListCreateAPIView

app_name = "strategy"

urlpatterns = [
    # path("", StrategyView.as_view(), name="home"),
    path("list/", StrategyListView.as_view(), name="strategy_list"),
    path("", StrategyListCreateAPIView.as_view(), name="strategy-list-create"),
]
