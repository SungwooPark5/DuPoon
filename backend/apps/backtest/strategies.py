import bt
import pandas as pd

from apps.stock.models import Price


def get_static_allocation_strategy(
    allocations: list[dict],
    period: str = "monthly",
    start_date: str = None,
    end_date: str = None,
) -> bt.Backtest:

    # 임의의 고정된 자산
    weights = {a["ticker"].ticker: a["weight"] for a in allocations}
    tickers = list(weights.keys())

    # 주가 데이터 조회
    prices = Price.objects.get_adj_close_dataframe(
        tickers=tickers, start_date=start_date, end_date=end_date
    )
    prices.dropna(inplace=True)  # 결측치 제거

    # 전략 정의
    strategy = bt.Strategy(
        "60/40 Allocation",
        [
            bt.algos.RunMonthly(),
            bt.algos.SelectAll(),
            bt.algos.WeighSpecified(**weights),
            bt.algos.Rebalance(),
        ],
    )

    return bt.Backtest(strategy, prices)
