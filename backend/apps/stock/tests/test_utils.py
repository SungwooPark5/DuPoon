import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from apps.stock.factories import StockFactory

fake_data = pd.DataFrame(
    [[37, 81, 81, 81, 81, 6100], [38, 82, 83, 83, 84, 10000]],
    index=pd.date_range("2022-01-01", periods=2),
    columns=pd.MultiIndex.from_tuples(
        [
            ("Adj Close", "TST"),
            ("Close", "TST"),
            ("High", "TST"),
            ("Low", "TST"),
            ("Open", "TST"),
            ("Volume", "TST"),
        ]
    ),
)
fake_data.index.name = "Date"
fake_data.columns.names = ["Price", "Ticker"]


@pytest.mark.django_db
@patch("apps.stock.utils.yf.download")
@patch("apps.stock.utils.Stock.objects.get_distinct_tickers")
def test_fetch_prices_for_all_stocks(mock_get_tickers, mock_download):
    mock_get_tickers.return_value = ["TST"]

    mock_download.return_value = fake_data
    from apps.stock.utils import fetch_prices_for_all_stocks

    prices, tickers = fetch_prices_for_all_stocks()

    assert tickers == ["TST"]
    assert isinstance(prices, pd.DataFrame)
    mock_download.assert_called_once()
    mock_get_tickers.assert_called_once()


@pytest.mark.django_db
@patch("apps.stock.utils.Price.objects.bulk_create")
def test_save_prices_to_db(mock_bulk_create):
    stock = StockFactory(ticker="TST")

    from apps.stock.utils import save_prices_to_db

    count, ticker_count = save_prices_to_db(fake_data, ["TST"])

    assert count == 2
    assert ticker_count == 1
    mock_bulk_create.assert_called_once()
