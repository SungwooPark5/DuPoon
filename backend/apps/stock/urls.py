from django.urls import path

from .views import StockListView, PriceListView

app_name = "stock"

urlpatterns = [
    path("stocks/", StockListView.as_view(), name="stock_list"),
    path("prices/", PriceListView.as_view(), name="price_list"),
]
