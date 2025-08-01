import pytest
from unittest.mock import patch, AsyncMock

from apps.stock.tasks import fetch_and_save_prices


@patch("apps.stock.tasks.get_channel_layer")
@patch("apps.stock.utils.save_prices_to_db")
@patch("apps.stock.utils.fetch_prices_for_all_stocks")
def test_fetch_and_save_prices_success(mock_fetch, mock_save, mock_channel_layer):
    mock_fetch.return_value = (["price1", "price2"], ["TST1", "TST2"])
    mock_save.return_value = (2, 2)

    mock_channel = AsyncMock()
    mock_channel_layer.return_value = mock_channel

    result = fetch_and_save_prices("test_user")

    # then
    mock_channel_layer.assert_called_once()
    mock_save.assert_called_once_with(["price1", "price2"], ["TST1", "TST2"])
    mock_channel.group_send(
        f"price_updates_{"test_user"}",
        {
            "type": "send_price_update",
            "message": "Prices fetched and saved successfully.",
        },
    )

    assert result is None
