import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.stock.models import Stock
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
    def test_create_stock(self, client):
        url = reverse("stock-list")
        data = {
            "name": "Test Stock",
            "ticker": "TST",
            "type": "stock",
            "market": "kospi",
            "listed_date": "2023-01-01",
        }
        response = client.post(url, data, format="json")

        assert response.status_code == 201
        assert Stock.objects.count() == 1
        assert Stock.objects.filter(ticker="TST").exists()

    def test_get_stock_list(self, client, stock):
        url = reverse("stock-list")
        response = client.get(url)
        data = response.json()

        assert response.status_code == 200
        assert data["results"][0]["ticker"] == stock.ticker
        assert len(data["results"]) == 1

    def test_get_stock_detail(self, client, stock):
        url = reverse("stock-detail", kwargs={"pk": stock.pk})
        response = client.get(url)
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
