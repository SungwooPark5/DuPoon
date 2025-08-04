import pytest
import factory
from datetime import date

from common.tests.base_model_test import CRUDTestMixin
from apps.stock.models import Stock, Price
from apps.stock.factories import StockFactory, PriceFactory

# Create your tests here.


@pytest.fixture
def stock():
    return Stock.objects.create(
        name="Test Stock",
        ticker="TST",
        type="stock",
        market="kospi",
        listed_date=date(2023, 1, 1),
    )


@pytest.mark.django_db
class TestStockModel(CRUDTestMixin):
    model = Stock

    def setup_method(self):
        self.sample_data = factory.build(dict, FACTORY_CLASS=StockFactory)
        self.sample_data_update = {
            "listed_date": date(2024, 1, 1),
        }


@pytest.mark.django_db
class TestPriceModel(CRUDTestMixin):
    model = Price

    def setup_method(self):
        self.stock = StockFactory()
        self.sample_data = factory.build(
            dict, FACTORY_CLASS=PriceFactory, stock=self.stock
        )
        self.sample_data_update = {
            "close_price": 150.00,
            "volume": 5000,
        }
