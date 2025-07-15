from dataclasses import dataclass
from typing import Optional


@dataclass
class BacktestConfig:
    allocations: list[dict]
    strategy_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    rebalance_freq: Optional[str] = "monthly"
    slippage: Optional[float] = 0.0
    include_cash: Optional[bool] = False
    cash_ticker: Optional[str] = "CASH"
    cash_weight: Optional[float] = 0.0

    def __post_init__(self):
        if self.strategy_name is None:
            self.strategy_name = "Custom Allocation"
