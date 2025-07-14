from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class StrategyView(TemplateView):
    template_name="strategy/home.html"