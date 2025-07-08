import bt
import pandas as pd

from apps.stock.models import Price
from .dtos import BacktestConfig


def get_static_allocation_strategy(
    config: BacktestConfig,
) -> bt.Backtest:
    """
    Create a backtest for a static asset allocation strategy.
    """

    # 임의의 고정된 자산
    weights = {a["ticker"].ticker: a["weight"] for a in config.allocations}
    tickers = list(weights.keys())

    # 주가 데이터 조회
    prices = Price.objects.get_adj_close_dataframe(
        tickers=tickers, start_date=config.start_date, end_date=config.end_date
    )
    prices.dropna(inplace=True)  # 결측치 제거

    # 리밸런싱 주기 설정
    run_alog = {
        "daily": bt.algos.RunDaily(),
        "weekly": bt.algos.RunWeekly(),
        "monthly": bt.algos.RunMonthly(),
        "quarterly": bt.algos.RunQuarterly(),
        "yearly": bt.algos.RunYearly(),
    }.get(config.rebalance_freq.lower())
    if run_alog is None:
        raise ValueError(f"Invalid rebalance frequency: {config.rebalance_freq}")

    # 전략 정의
    strategy = bt.Strategy(
        config.strategy_name,
        [
            run_alog,
            bt.algos.SelectAll(),
            bt.algos.WeighSpecified(**weights),
            bt.algos.Rebalance(),
        ],
    )

    return bt.Backtest(strategy, prices)
