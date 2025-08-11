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

    def test_get_strategy_list(self, api_client, strategy):
        url = reverse("strategy-list")
        response = api_client.get(url)
        data = response.json()
        results = data["results"]

        assert response.status_code == 200
        assert results[0]["name"] == strategy.name
        assert data["count"] == 1

    def test_get_strategy_detail(self, api_client, strategy):
        url = reverse("strategy-detail", kwargs={"pk": strategy.pk})
        data = {
            "name": "Updated Strategy",
            "description": "Updated",
            "type": "DYNAMIC",
        }
        response = api_client.put(url, data, format="json")

        assert response.status_code == 200
        strategy.refresh_from_db()
        assert strategy.name == "Updated Strategy"
        assert strategy.description == "Updated"
        assert strategy.type == "DYNAMIC"

    def test_update_strategy(self, api_client, strategy):
        pass

    def test_delete_strategy(self, api_client, strategy):
        pass
