from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from rest_framework import generics, viewsets

from .models import Strategy
from .serializers import StrategySerializer


# Create your views here.
class StrategyView(TemplateView):
    template_name = "strategy/home.html"


class StrategyListView(ListView):
    model = Strategy
    template_name = "strategy/strategy_list.html"
    context_object_name = "strategies"

    def get_queryset(self):
        return Strategy.objects.all().order_by("name")


# APIViews
class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
