from celery import shared_task

from .utils import fetch_prices_for_all_stocks, save_prices_to_db


@shared_task
def test_celery():
    """
    Celery task to test if the setup is working.
    """
    print("Celery is working!")
    return "Celery is working!"
