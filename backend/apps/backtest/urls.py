from django.urls import path

from .views import BacktestView

app_name = "backtest"

urlpatterns = [
    path("backtest/", BacktestView.as_view(), name="backtest"),
]
