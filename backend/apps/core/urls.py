from django.urls import path
from django.views.generic import RedirectView

from .views import home_page_view

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="backtest:backtest", permanent=True),
        name="home",
    ),
]
