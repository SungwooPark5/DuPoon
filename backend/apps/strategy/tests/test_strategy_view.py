import pytest
from django.urls import reverse
from django.test import Client

from apps.strategy.factories import StrategyFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def strategy():
    return StrategyFactory()


@pytest.mark.django_db
class TestStrategyListView:

    def test_strategy_list_view(self, client, strategy):
        url = reverse("strategy:strategy_list")
        response = client.get(url)

        assert response.status_code == 200
        assert strategy.name in response.content.decode()
        assert strategy.description in response.content.decode()
