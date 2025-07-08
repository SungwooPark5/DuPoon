import bt
import pandas as pd

from apps.stock.models import Price


def get_static_allocation_strategy(
    allocations: list[dict],
    strategy_name: str = "Custom Allocation",
    rebalance_freq: str = "monthly",  # "daily", "weekly", "monthly", "quarterly", "yearly"
    start_date: str = None,
    end_date: str = None,
    slippage: float = 0.0,
) -> bt.Backtest:
    """
    Create a backtest for a static asset allocation strategy.
    """

    # 임의의 고정된 자산
    weights = {a["ticker"].ticker: a["weight"] for a in allocations}
    tickers = list(weights.keys())

    # 주가 데이터 조회
    prices = Price.objects.get_adj_close_dataframe(
        tickers=tickers, start_date=start_date, end_date=end_date
    )
    prices.dropna(inplace=True)  # 결측치 제거

    # 리밸런싱 주기 설정
    run_alog = {
        "daily": bt.algos.RunDaily(),
        "weekly": bt.algos.RunWeekly(),
        "monthly": bt.algos.RunMonthly(),
        "quarterly": bt.algos.RunQuarterly(),
        "yearly": bt.algos.RunYearly(),
    }.get(rebalance_freq.lower())
    if run_alog is None:
        raise ValueError(f"Invalid rebalance frequency: {rebalance_freq}")

    # 전략 정의
    strategy = bt.Strategy(
        strategy_name,
        [
            run_alog,
            bt.algos.SelectAll(),
            bt.algos.WeighSpecified(**weights),
            bt.algos.Rebalance(),
        ],
    )

    return bt.Backtest(strategy, prices)
