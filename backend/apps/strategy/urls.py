from django.urls import path

from .views import StrategyView, StrategyListView, StrategyDetailView

app_name = "strategy"

urlpatterns = [
    # path("", StrategyView.as_view(), name="home"),
    path("list/", StrategyListView.as_view(), name="strategy_list"),
    path("detail/<int:pk>/", StrategyDetailView.as_view(), name="strategy_detail"),
]
