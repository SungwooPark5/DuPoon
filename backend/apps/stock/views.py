from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import OuterRef, Subquery

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Stock, Price
from . import tasks


# Create your views here.
class StockListView(ListView):
    model = Stock
    template_name = "stock/stock_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        # Annotate each stock with the latest price date
        latest_date = (
            Price.objects.filter(stock=OuterRef("pk"))
            .order_by("-date")
            .values("date")[:1]
        )
        return Stock.objects.annotate(latest_date=Subquery(latest_date))


class StockDetailView(DetailView):
    model = Stock
    template_name = "stock/stock_detail.html"
    context_object_name = "stock"

    def get_queryset(self):
        return Stock.objects.all()


class PriceListView(ListView):
    model = Price
    template_name = "stock/price_list.html"
    context_object_name = "prices"
    paginate_by = 10

    def get_queryset(self):
        return Price.objects.all().order_by("date")


# API views
class PriceFetchAPIView(APIView):
    """
    API view to start fetching prices for all stocks.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Start fetching prices for all stocks.
        """

        try:
            user_id = request.user.id
            tasks.fetch_and_save_prices.delay(str(user_id))
            return Response(
                {"message": "started fetching prices"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Error starting price fetch: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
