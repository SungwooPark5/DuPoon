import numpy as np
import pandas as pd


def create_slippage_fn(rate: float):
    """
    Create a slippage function that returns a fixed slippage value.
    :param rate: The slippage rate as a percentage (e.g., 0.01 for 1%).
    :return: A function that calculates slippage based on quantity and price.
    """

    def slippage_fn(q, p):
        return max(1, rate * abs(q))

    return slippage_fn


def generate_cash_series(
    dates: pd.DatetimeIndex, annual_rate: float = 0.0
) -> pd.Series:
    """
    Generate a cash series based on a given date range.
    param dates: The date range for the cash series.
    param annual_rate: The annual interest rate for the cash series.
    :return: A pandas Series representing the cash series.
    """

    daily_rate = (1 + annual_rate) ** (1 / 252) - 1
    cash_series = (1 + daily_rate) ** np.arange(len(dates))

    return pd.Series(cash_series, index=dates)
