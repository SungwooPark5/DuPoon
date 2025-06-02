from celery import shared_task

from . import utils


@shared_task
def test_celery():
    """
    Celery task to test if the setup is working.
    """
    print("Celery is working!")
    return "Celery is working!"


@shared_task
def fetch_and_save_prices():
    """
    Celery task to fetch stock prices and save them to the database.
    """
    try:
        prices, tickers = utils.fetch_prices_for_all_stocks()
        utils.save_prices_to_db(prices, tickers)

        print(
            f"Successfully fetched and saved {len(prices)} prices for {len(tickers)} stocks."
        )
        return f"Successfully fetched and saved {len(prices)} prices for {len(tickers)} stocks."

    except Exception as e:
        print(f"Error fetching and saving prices: {e}")
        return f"Error fetching and saving prices: {e}"
