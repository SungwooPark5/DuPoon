from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework import generics, viewsets

from .models import Strategy
from apps.backtest.models import BacktestStat
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


class StrategyDetailView(DetailView):
    model = Strategy
    template_name = "strategy/strategy_detail.html"
    context_object_name = "strategy"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["backtest_results"] = BacktestStat.objects.filter(strategy=self.object)

        return context


# APIViews
class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
