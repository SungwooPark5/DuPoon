import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient


from apps.stock.models import Stock, Price
from apps.stock.factories import StockFactory


@pytest.fixture
def api_client():
    """
    Fixture to provide an API client for testing.
    """
    return APIClient()


@pytest.mark.django_db
class TestStockAPI:

    @pytest.fixture
    def stock(self):
        return StockFactory()

    # fixture나 factory는 기존에 필요한 데이터가 있어야 할 때 사용함
    # 따라서 stock 생성 요청 테스트는 fixture를 사용하지 않음
    def test_create_stock(self, api_client):
        url = reverse("stock-list")
        data = {
            "name": "Test Stock",
            "ticker": "TST",
            "type": "stock",
            "market": "kospi",
            "listed_date": "2023-01-01",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert Stock.objects.count() == 1
        assert Stock.objects.filter(ticker="TST").exists()

    def test_get_stock_list(self, api_client, stock):
        url = reverse("stock-list")
        response = api_client.get(url)
        data = response.json()

        assert response.status_code == 200
        assert data["results"][0]["ticker"] == stock.ticker
        assert len(data["results"]) == 1

    def test_get_stock_detail(self, api_client, stock):
        url = reverse("stock-detail", kwargs={"pk": stock.pk})
        response = api_client.get(url)
        data = response.json()

        assert response.status_code == 200
        assert data["ticker"] == stock.ticker
        assert data["name"] == stock.name

    def test_update_stock(self, api_client, stock):
        url = reverse("stock-detail", kwargs={"pk": stock.pk})
        data = {
            "name": "Updated Stock",
            "ticker": "TST",
            "type": "etf",
            "market": "nasdaq",
            "listed_date": "2023-01-02",
        }
        response = api_client.put(url, data, format="json")

        assert response.status_code == 200
        stock.refresh_from_db()
        assert stock.name == "Updated Stock"
        assert stock.type == "etf"
        assert stock.market == "nasdaq"

    def test_delete_stock(self, api_client, stock):
        url = reverse("stock-detail", kwargs={"pk": stock.pk})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not Stock.objects.filter(pk=stock.pk).exists()


@pytest.mark.django_db
class TestPriceFetchAPI:

    @pytest.fixture
    def client(self, django_user_model):
        user = django_user_model.objects.create_user(
            username="testuser", password="testpass"
        )
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    # Integration test for fetch API
    @patch("apps.stock.utils.yf.download")
    def test_fetch_success(self, mock_download, fake_price_data_df, client):
        mock_download.return_value = fake_price_data_df
        StockFactory(ticker="TST")

        url = reverse("price_fetch")
        response = client.post(url)

        assert response.status_code == 200
        assert response.json()["message"] == "started fetching prices"

        # fake_price_data_df is in "apps/stock/tests/conftest.py"
        prices = Price.objects.filter(stock__ticker="TST")
        assert prices.count() == 2
        assert prices.first().stock.ticker == "TST"
        assert prices.first().adj_close_price in [37, 38]

    @patch(
        "apps.stock.tasks.fetch_and_save_prices.delay",
        side_effect=Exception("Fetch failed"),
    )
    def test_fetch_failure(self, mock_delay, client):
        url = reverse("price_fetch")
        response = client.post(url)

        assert response.status_code == 500
        assert response.json()["message"] == "Error starting price fetch: Fetch failed"
