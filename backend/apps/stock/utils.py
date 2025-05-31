import yfinance as yf
import pandas as pd

from apps.stock.models import Stock, Price
from datetime import datetime, timedelta


def fetch_prices_for_all_stocks():
    """
    Fetch historical stock data for all distinct stock tickers.
    """
    tickers = list(Stock.objects.get_distinct_tickers())
    prices = yf.download(tickers, auto_adjust=False)

    print(prices)

    print(Price.objects.get_latest_price_date(Stock.objects.get(ticker="SPY")))

    # return save_prices_to_db(prices, tickers)


def save_prices_to_db(prices: pd.DataFrame, tickers: list[str]) -> None:
    """
    Save the fetched stock data to the database.
    """
    if isinstance(prices.columns, pd.MultiIndex):

        for ticker in tickers:
            ticker_prices = prices.xs(ticker, level=1, axis=1)
            prices = []
            for date, row in ticker_prices.iterrows():
                price = Price(
                    stock=Stock.objects.get(ticker=ticker),
                    date=date,
                    open_price=row["Open"],
                    high_price=row["High"],
                    low_price=row["Low"],
                    close_price=row["Close"],
                    volume=row["Volume"],
                )
                prices.append(price)
