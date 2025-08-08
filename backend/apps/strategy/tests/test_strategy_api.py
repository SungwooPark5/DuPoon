import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from apps.strategy.models import Strategy
from apps.strategy.factories import StrategyFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestStrategyViewSet:

    @pytest.fixture
    def strategy(self):
        return StrategyFactory()

    def test_create_strategy(self, api_client):
        url = reverse("strategy-list")

        payload = {
            "name": "Test Strategy",
            "description": "Strategy for a create test",
            "type": "STATIC",
            "allocations": {"ticker": "TST", "weight": 1.0},
            "rebalance_frequency": "yearly",
            "include_cash": False,
        }

        response = api_client.post(url, payload, format="json")

        assert response.status_code == 201
        assert Strategy.objects.count() == 1
        assert Strategy.objects.filter(name="Test Strategy").exists()
