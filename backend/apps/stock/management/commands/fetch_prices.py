from django.core.management.base import BaseCommand
from apps.stock.utils import fetch_prices_for_all_stocks, save_prices_to_db


class Command(BaseCommand):
    help = "Fetch historical stock prices for all stocks"

    def handle(self, *args, **kwargs):
        """
        Fetch historical stock prices for all stocks and save them to the database.
        """
        try:
            prices, tickers = fetch_prices_for_all_stocks()
            save_prices_to_db(prices, tickers)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully fetched stock prices.\nSaved {len(prices)} prices for {len(tickers)} stocks."
                )
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error fetching stock prices: {e}"))
