from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Stock, Price


# Create your views here.
class StockListView(ListView):
    model = Stock
    template_name = "stock/stock_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        return Stock.objects.all().order_by("name")


class PriceListView(ListView):
    model = Price
    template_name = "stock/price_list.html"
    context_object_name = "prices"
    paginate_by = 10

    def get_queryset(self):
        return Price.objects.all().order_by("date")
