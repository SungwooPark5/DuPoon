from django.core.management.base import BaseCommand
from apps.stock.utils import fetch_prices_for_all_stocks


class Command(BaseCommand):
    help = "Fetch historical stock prices for all stocks"

    def handle(self, *args, **kwargs):
        """
        Fetch historical stock prices for all stocks and save them to the database.
        """
        try:
            fetch_prices_for_all_stocks()
            self.stdout.write(self.style.SUCCESS("Successfully fetched stock prices."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error fetching stock prices: {e}"))
