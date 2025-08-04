import pytest
from datetime import date

from apps.stock.models import Stock, Price
from apps.stock.factories import PriceFactory, StockFactory


@pytest.mark.django_db
class TestStockManager:
    def test_get_distinct_tickers(self):
        StockFactory(ticker="TST1")
        StockFactory(ticker="TST2")
        distinct_tickers = Stock.objects.get_distinct_tickers()
        assert list(distinct_tickers) == ["TST1", "TST2"]


@pytest.mark.django_db
class TestPriceManager:
    @pytest.fixture
    def stock(self):
        return StockFactory(ticker="TEST")

    @pytest.fixture
    def setup_prices(self, stock):
        PriceFactory(stock=stock, date="1999-01-01", adj_close_price=100.0)
        PriceFactory(stock=stock, date="2000-01-01", adj_close_price=150.0)
        PriceFactory(stock=stock, date="2020-01-01", adj_close_price=200.0)

    def test_get_latest_prices(self, stock, setup_prices):
        prices = Price.objects.get_latest_prices(stock)
        assert prices.count() == 3
        assert prices.first().adj_close_price == 200.0
        assert prices.first().date == date(2020, 1, 1)

    def test_get_latest_price_date(self, stock, setup_prices):
        latest_date = Price.objects.get_latest_price_date(stock=stock)
        assert latest_date == date(2020, 1, 1)

    def test_get_latest_price_date_returns_none_if_no_price(self, stock, setup_prices):
        no_price_stock = StockFactory(ticker="NOPRICE")
        no_price_date = Price.objects.get_latest_price_date(stock=no_price_stock)
        assert no_price_date is None

    def test_get_adj_close_dataframe(self, stock, setup_prices):
        price_df = Price.objects.get_adj_close_dataframe(tickers=stock.ticker)

        print(price_df)
        print(price_df.loc["1999-01-01", stock.ticker])
        print(len(price_df[stock.ticker]))

        assert price_df.loc["1999-01-01", stock.ticker] == 100.0
        assert len(price_df[stock.ticker]) == 3
