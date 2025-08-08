import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from apps.stock.factories import StockFactory


@pytest.mark.django_db
@patch("apps.stock.utils.yf.download")
@patch("apps.stock.utils.Stock.objects.get_distinct_tickers")
def test_fetch_prices_for_all_stocks(
    mock_get_tickers, mock_download, fake_price_data_df
):
    mock_get_tickers.return_value = ["TST"]

    mock_download.return_value = fake_price_data_df
    from apps.stock.utils import fetch_prices_for_all_stocks

    prices, tickers = fetch_prices_for_all_stocks()

    assert tickers == ["TST"]
    assert isinstance(prices, pd.DataFrame)
    mock_download.assert_called_once()
    mock_get_tickers.assert_called_once()


@pytest.mark.django_db
@patch("apps.stock.utils.Price.objects.bulk_create")
def test_save_prices_to_db(mock_bulk_create, fake_price_data_df):
    stock = StockFactory(ticker="TST")

    from apps.stock.utils import save_prices_to_db

    count, ticker_count = save_prices_to_db(fake_price_data_df, ["TST"])

    assert count == 2
    assert ticker_count == 1
    mock_bulk_create.assert_called_once()
