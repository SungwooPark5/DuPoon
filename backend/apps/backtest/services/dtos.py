from dataclasses import dataclass
from typing import Optional


@dataclass
class BacktestConfig:
    allocations: list[dict]
    strategy_name: Optional[str] = "Custom Allocation"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    rebalance_freq: Optional[str] = "monthly"
    slippage: Optional[float] = 0.0
