from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from . import utils


@shared_task
def test_celery():
    """
    Celery task to test if the setup is working.
    """
    print("Celery is working!")
    return "Celery is working!"


@shared_task
def fetch_and_save_prices(user_id: str):
    """
    Celery task to fetch stock prices and save them to the database.
    """
    try:
        prices, tickers = utils.fetch_prices_for_all_stocks()
        utils.save_prices_to_db(prices, tickers)

        # notify that the task was successful
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"price_updates_{user_id}",
            {
                "type": "send_price_update",
                "message": "Prices fetched and saved successfully.",
            },
        )
    except Exception as e:
        print(f"Error fetching and saving prices: {e}")
        return f"Error fetching and saving prices: {e}"
