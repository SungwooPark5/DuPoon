import pytest
from django.urls import reverse
from django.test import Client

from apps.stock.factories import StockFactory, PriceFactory


@pytest.mark.django_db
class TestStockListView:

    @pytest.fixture
    def stock(self):
        return StockFactory()

    @pytest.fixture
    def price(self, stock):
        return PriceFactory(stock=stock)

    def test_stock_list_view(self, client, stock, price):
        url = reverse("stock:stock_list")
        response = client.get(url)

        print(response.content.decode())

        assert response.status_code == 200
        assert stock.ticker in response.content.decode()
        assert stock.name in response.content.decode()
        # Latest price date should be displayed(e.g.: "2023년 1월 1일")
        price_date = price.date
        assert (
            f"{price_date.year}년 {price_date.month}월 {price_date.day}일"
            in response.content.decode()
        )
        # Test stock modal form
        assert (
            '<div class="modal fade" id="stockFormModal" tabindex="-1" aria-labelledby="stockFormModalLabel" aria-hidden="true">'
            in response.content.decode()
        )
