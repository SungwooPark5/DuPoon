import pytest
from django.urls import reverse
from django.test import Client

from apps.strategy.factories import StrategyFactory
from apps.backtest.factories import BacktestStatFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def strategy():
    return StrategyFactory()


@pytest.fixture
def backtest_result(strategy):
    return BacktestStatFactory(strategy=strategy)


@pytest.mark.django_db
class TestStrategyListView:

    def test_strategy_list_view(self, client, strategy):
        url = reverse("strategy:strategy_list")
        response = client.get(url)

        assert response.status_code == 200
        assert strategy.name in response.content.decode()
        assert strategy.description in response.content.decode()


@pytest.mark.django_db
class TestStrategyDetailView:

    def test_strategy_detail_strategy_infos(self, client, strategy):
        url = reverse("strategy:strategy_detail", args=[strategy.pk])
        response = client.get(url)

        assert response.status_code == 200
        assert strategy.name in response.content.decode()
        assert strategy.description in response.content.decode()
        assert strategy.rebalance_frequency in response.content.decode()

    def test_strategy_detail_with_backtest_result(
        self, client, strategy, backtest_result
    ):
        url = reverse("strategy:strategy_detail", args=[strategy.pk])
        response = client.get(url)

        assert response.status_code == 200
        assert strategy.name in response.content.decode()
        assert strategy.description in response.content.decode()
        assert strategy.rebalance_frequency in response.content.decode()

        # Backtest stats
        assert f"{backtest_result.sharpe_ratio:.2f}" in response.content.decode()
        assert f"{backtest_result.max_drawdown*100:.2f}%" in response.content.decode()
        assert f"{backtest_result.cagr*100:.2f}%" in response.content.decode()
