import pytest
import pandas as pd
import apps.backtest.utils as backtest_utils


def test_create_slippage_fn():
    # Test with a slippage rate of 0.01 (1%)
    slippage_fn = backtest_utils.create_slippage_fn(0.01)

    # Test with a positive quantity and price
    assert slippage_fn(100, 50) == 1.0  # 1% of 100 is 1.0

    # Test with a negative quantity
    assert slippage_fn(-100, 50) == 1.0  # Should still return 1.0

    # Test with zero quantity
    assert slippage_fn(0, 50) == 1.0  # Should return 1.0 as per the max condition


def test_generate_cash_series():
    # Test with a date range and an annual rate of 0.05 (5%)
    dates = pd.date_range(start="2023-01-01", periods=10, freq="D")
    cash_series = backtest_utils.generate_cash_series(dates, annual_rate=0.05)

    # Check if the length of the series matches the number of dates
    assert len(cash_series) == len(dates)

    # Check if the first value is 1 (initial cash value)
    assert cash_series.iloc[0] == 1.0

    # Check if the last value is greater than the first value due to interest accumulation
    assert cash_series.iloc[-1] > cash_series.iloc[0]
    # Check if the series is a pandas Series
    assert isinstance(cash_series, pd.Series)
