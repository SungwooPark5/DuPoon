import yfinance as yf

from apps.stock.models import Stock, Price
from datetime import datetime, timedelta


def fetch_prices_for_all_stocks(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker symbol between specified dates.

    :param ticker: Stock ticker symbol (e.g., 'AAPL' for Apple Inc.)
    :param start_date: Start date in 'YYYY-MM-DD' format
    :param end_date: End date in 'YYYY-MM-DD' format
    :return: DataFrame containing stock data
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    return stock_data


# Example usage:
if __name__ == "__main__":
    # Fetch historical prices for SPY (S&P 500 ETF) from January 1, 2023 to October 1, 2023
    fetch_stock_data = fetch_prices_for_all_stocks("SPY", "2023-01-01", "2023-10-01")
    print(fetch_stock_data.head())  # Display the first few rows of the fetched data
