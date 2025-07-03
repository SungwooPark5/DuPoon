import bt
import pandas as pd

from apps.stock.models import Price, Stock
from common.utils import convert_queryset_to_dataframe


def get_static_allocation_strategy():

    # 임의의 고정된 자산
    tickers = ["SPY", "TLT"]
    weights = {"SPY": 0.6, "TLT": 0.4}

    # 주가 데이터 조회
    prices = Price.objects.get_adj_close_dataframe(tickers=tickers)
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
