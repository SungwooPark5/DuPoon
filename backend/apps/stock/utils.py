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

    # print(prices)

    # print(Price.objects.get_latest_price_date(Stock.objects.get(ticker="SPY")))

    return save_prices_to_db(prices, tickers)


def save_prices_to_db(prices: pd.DataFrame, tickers: list[str]) -> list[int]:
    """
    Save the fetched stock data to the database.
    """

    price_list = []

    if isinstance(tickers, list):
        tickers = [ticker.upper() for ticker in tickers]
    else:
        tickers = [tickers.upper()]

    for ticker in tickers:
        # print(prices)
        ticker_prices = prices.xs(ticker, level=1, axis=1).copy()
        ticker_prices.dropna(inplace=True)
        stock = Stock.objects.get(ticker=ticker)
        # print(ticker, ticker_prices)
        for date, row in ticker_prices.iterrows():
            price_list.append(
                Price(
                    stock=stock,
                    date=date,
                    open_price=row["Open"],
                    high_price=row["High"],
                    low_price=row["Low"],
                    close_price=row["Close"],
                    adj_close_price=row["Adj Close"],
                    volume=row["Volume"],
                )
            )

    Price.objects.bulk_create(price_list, ignore_conflicts=True)

    return len(price_list), len(tickers)
