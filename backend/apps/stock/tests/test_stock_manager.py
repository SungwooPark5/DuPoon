import pytest
from datetime import date

from apps.stock.models import Stock
from apps.stock.factories import StockFactory


@pytest.mark.django_db
def test_get_distinct_tickers():
    StockFactory(ticker="TST1")
    StockFactory(ticker="TST2")
    distinct_tickers = Stock.objects.get_distinct_tickers()
    assert list(distinct_tickers) == ["TST1", "TST2"]
