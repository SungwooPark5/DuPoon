import pytest
from django.urls import reverse
from django.test import Client

from apps.strategy.factories import StrategyFactory


@pytest.mark.django_db
class TestBacktestView:
    @pytest.fixture
    def strategy(self):
        return StrategyFactory()

    def test_backtest_view(self, client, strategy):
        """
        Test the backtest view rendering.
        """
        url = reverse("backtest:backtest")
        response = client.get(url)

        assert response.status_code == 200
        assert '<form id="backtest-form"' in response.content.decode()
        assert '<input type="text" id="strategy_id"' in response.content.decode()
