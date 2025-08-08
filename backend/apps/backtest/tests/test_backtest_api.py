import pytest
import pandas as pd

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.stock.factories import StockFactory, PriceFactory
from apps.strategy.factories import StrategyFactory
from apps.backtest.factories import BacktestStatFactory
from apps.backtest.models import BacktestStat


@pytest.fixture
def auth_api_client():
    """
    Fixture to provide an API client for testing.
    """

    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpass")
    client.force_authenticate(user=user)

    return client


@pytest.fixture
def stock():
    """
    Fixture to create a stock instance for testing.
    """
    return StockFactory(ticker="TST1")


@pytest.mark.django_db
class TestBacktestAPI:
    def test_request_backtest(self, auth_api_client, stock):
        PriceFactory(stock=stock, date="2020-01-01", adj_close_price=100.0)
        PriceFactory(stock=stock, date="2020-02-01", adj_close_price=105.0)
        PriceFactory(stock=stock, date="2020-03-01", adj_close_price=110.0)

        url = reverse("static_allocation_backtest")
        payload = {
            "strategy_name": "Test Strategy",
            "start_date": "2020-01-01",
            "end_date": "2020-03-01",
            "rebalance_freq": "monthly",
            "allocations": [{"ticker": stock.ticker, "weight": 1.0}],
        }
        response = auth_api_client.post(url, payload, format="json")
        data = response.data
        stats = data.get("stats", {})
        print(data)

        assert response.status_code == 200
        assert data["name"] == "Test Strategy"
        assert stats["cagr"] is not None
        assert stats["start"] == pd.Timestamp("2019-12-31")


@pytest.mark.django_db
class TestBacktestStatAPI:
    @pytest.fixture
    def strategy(self):
        return StrategyFactory(name="Test Strategy")

    @pytest.fixture
    def backtest_stat(self, strategy):
        return BacktestStatFactory(strategy=strategy)

    def test_create_backtest_stat(self, auth_api_client, strategy):
        url = reverse("backtest-stats-list")
        data = {
            "strategy": strategy.id,
            "name": "Test Backtest Stat",
            "description": "This is a test backtest stat.",
            "start_date": "2020-01-01",
            "end_date": "2020-12-31",
            "total_return": 1.2,
            "cagr": 0.1,
            "max_drawdown": 0.2,
            "volatility": 0.15,
            "sharpe_ratio": 1.5,
            "sortino_ratio": 1.8,
        }
        response = auth_api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert response.data["name"] == "Test Backtest Stat"
        assert BacktestStat.objects.count() == 1
        assert BacktestStat.objects.first().strategy == strategy

    def test_get_backtest_stat_list(self, auth_api_client, backtest_stat):
        url = reverse("backtest-stats-list")
        response = auth_api_client.get(url)
        data = response.data

        print(data)

        assert response.status_code == 200
        assert data["count"] == 1
        assert data["results"][0]["name"] == backtest_stat.name
        assert data["results"][0]["strategy"] == backtest_stat.strategy.id

    def test_get_backtest_stat_detail(self, auth_api_client, backtest_stat):
        url = reverse("backtest-stats-detail", kwargs={"pk": backtest_stat.pk})
        response = auth_api_client.get(url)
        data = response.data

        assert response.status_code == 200
        assert data["name"] == backtest_stat.name
        assert data["strategy"] == backtest_stat.strategy.id

    def test_update_backtest_stat(self, auth_api_client, backtest_stat):
        """
        PATCH request to update backtest_stat
        """
        url = reverse("backtest-stats-detail", kwargs={"pk": backtest_stat.pk})
        data = {
            "name": "Updated Backtest Stat",
            "description": "Updated description.",
            "total_return": 1.5,
        }
        response = auth_api_client.patch(url, data, format="json")

        print(response.data)

        assert response.status_code == 200
        assert response.data["name"] == "Updated Backtest Stat"
        assert response.data["description"] == "Updated description."
        assert response.data["total_return"] == 1.5

    def test_delete_backtest_stat(self, auth_api_client, backtest_stat):
        url = reverse("backtest-stats-detail", kwargs={"pk": backtest_stat.pk})
        response = auth_api_client.delete(url)

        assert response.status_code == 204
        assert BacktestStat.objects.count() == 0
        assert not BacktestStat.objects.filter(pk=backtest_stat.pk).exists()
