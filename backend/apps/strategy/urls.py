from django.urls import path

from .views import StrategyView

app_name = "strategy"

urlpatterns =[
    path("", StrategyView.as_view(), name="home")
]